# SPDX-License-Identifier: GPL-3.0-or-later

"""
euserv 自动续期脚本
功能:
* 支持 TrueCaptcha API 和 LLM OCR 两种验证码识别方式
* 发送通知到 Telegram
* 增加登录失败重试机制
* 日志信息格式化
"""
import os
import re
import json
import time
import base64
import io
import requests
from bs4 import BeautifulSoup

# 账户信息：用户名和密码
USERNAME = os.getenv('EUSERV_USERNAME')  # 填写用户名或邮箱
PASSWORD = os.getenv('EUSERV_PASSWORD')  # 填写密码

# 验证码识别方式配置
# 支持: 'truecaptcha' 或 'llm'
CAPTCHA_SOLVER_TYPE = (os.getenv('CAPTCHA_SOLVER_TYPE', '').strip() or 'llm').lower()

# TrueCaptcha API 配置
TRUECAPTCHA_USERID = os.getenv('TRUECAPTCHA_USERID')
TRUECAPTCHA_APIKEY = os.getenv('TRUECAPTCHA_APIKEY')

# OpenAI API 配置（用于 LLM OCR）
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
_raw_openai_base_url = os.getenv('OPENAI_BASE_URL')
if _raw_openai_base_url is not None:
    OPENAI_BASE_URL = _raw_openai_base_url.strip() or None
    if OPENAI_BASE_URL is None:
        os.environ.pop('OPENAI_BASE_URL', None)
else:
    OPENAI_BASE_URL = None
OPENAI_MODEL = os.getenv('OPENAI_MODEL') or 'gpt-4o-mini'  # 默认使用 gpt-4o-mini

# Mailparser 配置
MAILPARSER_DOWNLOAD_URL_ID = os.getenv('MAILPARSER_DOWNLOAD_URL_ID')
MAILPARSER_DOWNLOAD_BASE_URL = "https://files.mailparser.io/d/"

# 推送方式配置
# 支持: 'telegram' 或 'gotify'
PUSH_TYPE = (os.getenv('PUSH_TYPE', '').strip() or 'telegram').lower()

# Telegram Bot 推送配置
TG_BOT_TOKEN = os.getenv('TG_BOT_TOKEN')
TG_USER_ID = os.getenv('TG_USER_ID')
TG_API_HOST = "https://api.telegram.org"

# Gotify 推送配置
GOTIFY_URL = os.getenv('GOTIFY_URL')  # 例如: https://push.example.com
GOTIFY_TOKEN = os.getenv('GOTIFY_TOKEN')

# 代理设置（如果需要）
## PROXIES = {"http": "http://127.0.0.1:10808", "https": "http://127.0.0.1:10808"}

# 最大登录重试次数
LOGIN_MAX_RETRY_COUNT = 10

# 接收 PIN 的等待时间，单位为秒
def get_int_env(name: str, default: int) -> int:
    value = os.getenv(name)
    if value is None or value.strip() == "":
        return default
    try:
        return int(value.strip())
    except ValueError:
        print(f"[AutoEUServerless] 环境变量 {name}={value!r} 不是有效整数，使用默认值 {default}")
        return default

WAITING_TIME_OF_PIN = get_int_env('WAITING_TIME_OF_PIN', 60)

# 从 Mailparser 获取 PIN 的重试配置，避免邮件尚未解析完成时因空列表直接崩溃
MAILPARSER_PIN_MAX_RETRIES = get_int_env('MAILPARSER_PIN_MAX_RETRIES', 6)
MAILPARSER_PIN_RETRY_DELAY = get_int_env('MAILPARSER_PIN_RETRY_DELAY', 30)

# LLM OCR 配置
OCR_MAX_RETRIES = 10  # OCR API 调用最大重试次数
OCR_RETRY_DELAY = 5  # OCR 重试延迟（秒）
OCR_IMAGE_MAX_SIZE = (300, 100)  # OCR 图片缩放最大尺寸

# 是否检查 TrueCaptcha 使用情况
CHECK_CAPTCHA_SOLVER_USAGE = True

user_agent = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/95.0.4638.69 Safari/537.36"
)
desp = ""  # 日志信息

def log(info: str):
    emoji_map = {
        "正在续费": "🔄",
        "检测到": "🔍",
        "ServerID": "🔗",
        "无需更新": "✅",
        "续订错误": "⚠️",
        "已成功续订": "🎉",
        "所有工作完成": "🏁",
        "登陆失败": "❗",
        "验证通过": "✔️",
        "验证失败": "❌",
        "API 使用次数": "📊",
        "验证码是": "🔢",
        "登录尝试": "🔑",
        "[MailParser]": "📧",
        "[TrueCaptcha]": "🧩",
        "[LLM OCR]": "🧩",
        "[Captcha Solver]": "🧩",
        "[AutoEUServerless]": "🌐",
    }
    # 对每个关键字进行检查，并在找到时添加 emoji
    for key, emoji in emoji_map.items():
        if key in info:
            info = emoji + " " + info
            break

    print(info)
    global desp
    desp += info + "\n\n"


# 登录重试装饰器
def login_retry(*args, **kwargs):
    def wrapper(func):
        def inner(username, password):
            ret, ret_session = func(username, password)
            max_retry = kwargs.get("max_retry")
            # 默认重试 3 次
            if not max_retry:
                max_retry = 3
            number = 0
            if ret == "-1":
                while number < max_retry:
                    number += 1
                    if number > 1:
                        log("[AutoEUServerless] 登录尝试第 {} 次".format(number))
                    sess_id, session = func(username, password)
                    if sess_id != "-1":
                        return sess_id, session
                    else:
                        if number == max_retry:
                            return sess_id, session
            else:
                return ret, ret_session
        return inner
    return wrapper

# ========== TrueCaptcha 验证码解决器 ==========
def truecaptcha_solver(captcha_image_url: str, session: requests.session) -> dict:
    response = session.get(captcha_image_url)
    encoded_string = base64.b64encode(response.content)
    url = "https://api.apitruecaptcha.org/one/gettext"

    data = {
        "userid": TRUECAPTCHA_USERID,
        "apikey": TRUECAPTCHA_APIKEY,
        "case": "mixed",
        "mode": "human",
        "data": str(encoded_string)[2:-1],
    }
    r = requests.post(url=url, json=data)
    j = json.loads(r.text)
    return j

def get_captcha_solver_usage() -> dict:
    url = "https://api.apitruecaptcha.org/one/getusage"
    params = {
        "username": TRUECAPTCHA_USERID,
        "apikey": TRUECAPTCHA_APIKEY,
    }
    r = requests.get(url=url, params=params)
    j = json.loads(r.text)
    return j

def handle_truecaptcha_result(solved: dict) -> str:
    if "result" in solved:
        solved_text = solved["result"]
        if "RESULT  IS" in solved_text:
            log("[TrueCaptcha] 使用的是演示 apikey。")
            text = re.findall(r"RESULT  IS . (.*) .", solved_text)[0]
        else:
            log("[TrueCaptcha] 使用的是您自己的 apikey。")
            text = solved_text
        operators = ["X", "x", "+", "-"]
        if any(x in text for x in operators):
            for operator in operators:
                operator_pos = text.find(operator)
                if operator == "x" or operator == "X":
                    operator = "*"
                if operator_pos != -1:
                    left_part = text[:operator_pos]
                    right_part = text[operator_pos + 1:]
                    if left_part.isdigit() and right_part.isdigit():
                        return str(eval(f"{left_part} {operator} {right_part}"))
                    else:
                        return text
        else:
            return text
    else:
        print(solved)
        raise KeyError("未找到解析结果。")

# ========== LLM OCR 验证码解决器 ==========
def resize_image(image_data: bytes, max_size=OCR_IMAGE_MAX_SIZE) -> bytes:
    from PIL import Image
    with Image.open(io.BytesIO(image_data)) as img:
        img.thumbnail(max_size)
        buffered = io.BytesIO()
        img.save(buffered, format="PNG")
    return buffered.getvalue()

def encode_image_to_base64(image_data: bytes) -> str:
    return base64.b64encode(image_data).decode('utf-8')

def invoke_llm_ocr(encoded_image: str) -> str:
    if not OPENAI_API_KEY:
        raise ValueError("未设置 OPENAI_API_KEY 环境变量")
    
    from openai import OpenAI
    
    client_kwargs = {"api_key": OPENAI_API_KEY}
    if OPENAI_BASE_URL:
        base_url = OPENAI_BASE_URL
        if not base_url.lower().startswith(('http://', 'https://')):
            base_url = f"https://{base_url}"
            log(f"[LLM OCR] 自动为 base_url 添加 https:// 协议前缀")
        client_kwargs["base_url"] = base_url
        log(f"[LLM OCR] 使用自定义 base_url: {base_url}")
    
    client = OpenAI(**client_kwargs)
    
    for attempt in range(OCR_MAX_RETRIES):
        try:
            completion = client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "text", 
                                "text": "请对这张验证码图片进行OCR识别。这是一个简单的数学算式验证码，可能包含加法(+)、减法(-)或乘法(X/x)运算。请直接输出算式结果的数字，不要输出其他内容。"
                            },
                            {
                                "type": "image_url", 
                                "image_url": {"url": f"data:image/png;base64,{encoded_image}"}
                            }
                        ]
                    }
                ],
                max_tokens=300,
            )
            result = completion.choices[0].message.content.strip()
            return result
        except Exception as e:
            log(f"[LLM OCR] 尝试 {attempt + 1} 失败: {e}")
            if attempt < OCR_MAX_RETRIES - 1:
                time.sleep(OCR_RETRY_DELAY)
            else:
                log("[LLM OCR] 达到最大重试次数，OCR 识别失败")
                raise

def llm_ocr_solver(captcha_image_url: str, session: requests.session) -> str:
    response = session.get(captcha_image_url)
    resized_image_data = resize_image(response.content)
    encoded_image = encode_image_to_base64(resized_image_data)
    result = invoke_llm_ocr(encoded_image)
    return result

def handle_llm_ocr_result(solved_text: str) -> str:
    cleaned_text = solved_text.replace("-", "").replace(" ", "").strip()
    
    operators = ["X", "x", "*", "+", "-"]
    for operator in operators:
        operator_pos = cleaned_text.find(operator)
        if operator_pos != -1:
            left_part = cleaned_text[:operator_pos]
            right_part = cleaned_text[operator_pos + 1:]
            
            if left_part.isdigit() and right_part.isdigit():
                actual_operator = "*" if operator in ["X", "x", "*"] else operator
                try:
                    result = eval(f"{left_part} {actual_operator} {right_part}")
                    return str(result)
                except:
                    pass
    
    if cleaned_text.isdigit():
        return cleaned_text
    
    return solved_text

# ========== 验证码解决器统一入口 ==========
def captcha_solver(captcha_image_url: str, session: requests.session):
    if CAPTCHA_SOLVER_TYPE == 'truecaptcha':
        log("[Captcha Solver] 使用 TrueCaptcha 进行验证码识别...")
        if not TRUECAPTCHA_USERID or not TRUECAPTCHA_APIKEY:
            raise ValueError("使用 TrueCaptcha 需要设置 TRUECAPTCHA_USERID 和 TRUECAPTCHA_APIKEY")
        solved_result = truecaptcha_solver(captcha_image_url, session)
        captcha_code = handle_truecaptcha_result(solved_result)
        log(f"[TrueCaptcha] 识别的验证码是: {captcha_code}")
        
        if CHECK_CAPTCHA_SOLVER_USAGE:
            try:
                usage = get_captcha_solver_usage()
                log(f"[TrueCaptcha] 当前日期 {usage[0]['date']} API 使用次数: {usage[0]['count']}")
            except:
                pass
        
        return captcha_code
    elif CAPTCHA_SOLVER_TYPE == 'llm':
        log("[Captcha Solver] 使用 LLM OCR 进行验证码识别...")
        if not OPENAI_API_KEY:
            raise ValueError("使用 LLM OCR 需要设置 OPENAI_API_KEY")
        solved_result = llm_ocr_solver(captcha_image_url, session)
        captcha_code = handle_llm_ocr_result(solved_result)
        log(f"[LLM OCR] 识别的验证码是: {captcha_code}")
        return captcha_code
    else:
        raise ValueError(f"不支持的验证码识别方式: {CAPTCHA_SOLVER_TYPE}，请设置为 'truecaptcha' 或 'llm'")

# 从 Mailparser 获取 PIN
def get_pin_from_mailparser(url_id: str) -> str:
    # 从 Mailparser 获取 PIN# 
    last_error = None
    download_url = f"{MAILPARSER_DOWNLOAD_BASE_URL}{url_id}"

    for attempt in range(1, MAILPARSER_PIN_MAX_RETRIES + 1):
        try:
            response = requests.get(download_url, timeout=30)
            response.raise_for_status()
            payload = response.json()

            if isinstance(payload, list) and payload:
                pin = payload[0].get("pin")
                if pin:
                    return str(pin).strip()
                last_error = "Mailparser 返回了数据，但第一条记录缺少 pin 字段"
            else:
                last_error = f"Mailparser 暂无 PIN 数据，返回记录数: {len(payload) if isinstance(payload, list) else '非列表响应'}"
        except Exception as exc:
            last_error = str(exc)

        if attempt < MAILPARSER_PIN_MAX_RETRIES:
            log(
                f"[MailParser] 第 {attempt}/{MAILPARSER_PIN_MAX_RETRIES} 次获取 PIN 失败: "
                f"{last_error}，{MAILPARSER_PIN_RETRY_DELAY} 秒后重试"
            )
            time.sleep(MAILPARSER_PIN_RETRY_DELAY)

    raise RuntimeError(
        "Mailparser 未返回可用 PIN。请检查 MAILPARSER_DOWNLOAD_URL_ID 是否正确、"
        "EUserv PIN 邮件是否已送达并被 Mailparser 规则解析，以及 Mailparser 输出字段是否命名为 pin。"
        f"最后一次错误: {last_error}"
    )

# 登录函数
@login_retry(max_retry=LOGIN_MAX_RETRY_COUNT)
def login(username: str, password: str) -> (str, requests.session):
    # 登录 EUserv 并获取 session# 
    headers = {"user-agent": user_agent, "origin": "https://www.euserv.com"}
    url = "https://support.euserv.com/index.iphp"
    captcha_image_url = "https://support.euserv.com/securimage_show.php"
    session = requests.Session()

    sess = session.get(url, headers=headers)
    sess_id = re.findall("PHPSESSID=(\\w{10,100});", str(sess.headers))[0]
    session.get("https://support.euserv.com/pic/logo_small.png", headers=headers)

    login_data = {
        "email": username,
        "password": password,
        "form_selected_language": "en",
        "Submit": "Login",
        "subaction": "login",
        "sess_id": sess_id,
    }
    f = session.post(url, headers=headers, data=login_data)
    f.raise_for_status()

    if "Hello" not in f.text and "Confirm or change your customer data here" not in f.text:
        if "To finish the login process please solve the following captcha." not in f.text:
            return "-1", session
        else:
            captcha_code = captcha_solver(captcha_image_url, session)

            f2 = session.post(
                url,
                headers=headers,
                data={
                    "subaction": "login",
                    "sess_id": sess_id,
                    "captcha_code": captcha_code,
                },
            )
            if "To finish the login process please solve the following captcha." not in f2.text:
                log("[Captcha Solver] 验证通过")
                return sess_id, session
            else:
                log("[Captcha Solver] 验证失败")
                return "-1", session
    else:
        return sess_id, session

# 获取服务器列表
def get_servers(sess_id: str, session: requests.session) -> {}:
    # 获取服务器列表# 
    d = {}
    url = "https://support.euserv.com/index.iphp?sess_id=" + sess_id
    headers = {"user-agent": user_agent, "origin": "https://www.euserv.com"}
    f = session.get(url=url, headers=headers)
    f.raise_for_status()
    soup = BeautifulSoup(f.text, "html.parser")
    for tr in soup.select(
        "#kc2_order_customer_orders_tab_content_1 .kc2_order_table.kc2_content_table tr"
    ):
        server_id = tr.select(".td-z1-sp1-kc")
        if not len(server_id) == 1:
            continue
        flag = (
            True
            if tr.select(".td-z1-sp2-kc .kc2_order_action_container")[0]
            .get_text()
            .find("Contract extension possible from")
            == -1
            else False
        )
        d[server_id[0].get_text()] = flag
    return d

# 续期操作
def renew(
    sess_id: str, session: requests.session, password: str, order_id: str, mailparser_dl_url_id: str
) -> bool:
    # 执行续期操作# 
    url = "https://support.euserv.com/index.iphp"
    headers = {
        "user-agent": user_agent,
        "Host": "support.euserv.com",
        "origin": "https://support.euserv.com",
        "Referer": "https://support.euserv.com/index.iphp",
    }
    data = {
        "Submit": "Extend contract",
        "sess_id": sess_id,
        "ord_no": order_id,
        "subaction": "choose_order",
        "choose_order_subaction": "show_contract_details",
    }
    session.post(url, headers=headers, data=data)

    # 弹出 'Security Check' 窗口，将自动触发 '发送 PIN'。
    session.post(
        url,
        headers=headers,
        data={
            "sess_id": sess_id,
            "subaction": "show_kc2_security_password_dialog",
            "prefix": "kc2_customer_contract_details_extend_contract_",
            "type": "1",
        },
    )

    # 等待邮件解析器解析出 PIN
    time.sleep(WAITING_TIME_OF_PIN)
    try:
        pin = get_pin_from_mailparser(mailparser_dl_url_id)
    except RuntimeError as exc:
        log(f"[MailParser] 获取 PIN 失败: {exc}")
        return False
    log(f"[MailParser] PIN: {pin}")

    # 使用 PIN 获取 token
    data = {
        "auth": pin,
        "sess_id": sess_id,
        "subaction": "kc2_security_password_get_token",
        "prefix": "kc2_customer_contract_details_extend_contract_",
        "type": 1,
        "ident": f"kc2_customer_contract_details_extend_contract_{order_id}",
    }
    f = session.post(url, headers=headers, data=data)
    f.raise_for_status()
    if not json.loads(f.text)["rs"] == "success":
        return False
    token = json.loads(f.text)["token"]["value"]
    data = {
        "sess_id": sess_id,
        "ord_id": order_id,
        "subaction": "kc2_customer_contract_details_extend_contract_term",
        "token": token,
    }
    session.post(url, headers=headers, data=data)
    time.sleep(5)
    return True

# 检查续期状态
def check(sess_id: str, session: requests.session):
    # 检查续期状态# 
    print("Checking.......")
    d = get_servers(sess_id, session)
    flag = True
    for key, val in d.items():
        if val:
            flag = False
            log("[AutoEUServerless] ServerID: %s 续期失败!" % key)

    if flag:
        log("[AutoEUServerless] 所有工作完成！尽情享受~")

# 发送 Telegram 通知
def telegram():
    message = (
        "<b>AutoEUServerless 日志</b>\n\n" + desp
    )

    # 请不要删除本段版权声明, 开发不易, 感谢! 感谢!
    # 请勿二次售卖,出售,开源不易,万分感谢!
    data = {
        "chat_id": TG_USER_ID,
        "text": message,
        "parse_mode": "HTML",
        "disable_web_page_preview": "true"
    }
    response = requests.post(
        TG_API_HOST + "/bot" + TG_BOT_TOKEN + "/sendMessage", data=data
    )
    if response.status_code != 200:
        print("Telegram Bot 推送失败")
    else:
        print("Telegram Bot 推送成功")

# 发送 Gotify 通知
def gotify():
    message = (
        "**AutoEUServerless 日志**\n\n" + desp
    )

    url = f"{GOTIFY_URL}/message?token={GOTIFY_TOKEN}"
    payload = {
        "message": message,
        "priority": 5,
        "extras": {
            "client::display": {
                "contentType": "text/markdown"
            }
        }
    }
    response = requests.post(url, json=payload)
    if response.status_code != 200:
        print("Gotify 推送失败")
    else:
        print("Gotify 推送成功")



def main_handler(event, context):
    # 主函数，处理每个账户的续期# 
    if not USERNAME or not PASSWORD:
        log("[AutoEUServerless] 你没有添加任何账户")
        exit(1)
    user_list = USERNAME.strip().split()
    passwd_list = PASSWORD.strip().split()
    mailparser_dl_url_id_list = MAILPARSER_DOWNLOAD_URL_ID.strip().split()
    if len(user_list) != len(passwd_list):
        log("[AutoEUServerless] 用户名和密码数量不匹配!")
        exit(1)
    if len(mailparser_dl_url_id_list) != len(user_list):
        log("[AutoEUServerless] mailparser_dl_url_ids 和用户名的数量不匹配!")
        exit(1)
    for i in range(len(user_list)):
        print("*" * 30)
        log("[AutoEUServerless] 正在续费第 %d 个账号" % (i + 1))
        sessid, s = login(user_list[i], passwd_list[i])
        if sessid == "-1":
            log("[AutoEUServerless] 第 %d 个账号登陆失败，请检查登录信息" % (i + 1))
            continue
        SERVERS = get_servers(sessid, s)
        log("[AutoEUServerless] 检测到第 {} 个账号有 {} 台 VPS，正在尝试续期".format(i + 1, len(SERVERS)))
        for k, v in SERVERS.items():
            if v:
                if not renew(sessid, s, passwd_list[i], k, mailparser_dl_url_id_list[i]):
                    log("[AutoEUServerless] ServerID: %s 续订错误!" % k)
                else:
                    log("[AutoEUServerless] ServerID: %s 已成功续订!" % k)
            else:
                log("[AutoEUServerless] ServerID: %s 无需更新" % k)
        time.sleep(15)
        check(sessid, s)
        time.sleep(5)

    # 发送推送通知
    if PUSH_TYPE == 'gotify':
        if GOTIFY_URL and GOTIFY_TOKEN:
            gotify()
        else:
            print("Gotify 推送配置不完整，跳过推送")
    else:  # 默认使用 telegram
        if TG_BOT_TOKEN and TG_USER_ID and TG_API_HOST:
            telegram()
        else:
            print("Telegram 推送配置不完整，跳过推送")

    print("*" * 30)

if __name__ == "__main__":
     main_handler(None, None)
