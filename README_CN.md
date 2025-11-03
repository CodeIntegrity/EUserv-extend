# EUserv-extend 自动续期脚本

[English](README.md) | 简体中文

## 📖 项目简介

这是一个基于 Python 3 的自动化脚本，用于自动续订 EUserv 服务器合约。该脚本通过 GitHub Actions 定时执行，无需手动干预即可完成续期操作。

### 主要特性

- ✅ **自动登录**: 自动处理 EUserv 客户面板登录
- 🧩 **验证码识别**: 集成 TrueCaptcha API 自动识别登录验证码
- 📧 **PIN 码获取**: 通过 Mailparser 自动获取邮箱中的安全 PIN 码
- 🔄 **自动续期**: 自动检测并续订即将到期的服务器合约
- 👥 **多账户支持**: 支持批量处理多个 EUserv 账户
- 📱 **Telegram 通知**: 运行结果通过 Telegram Bot 实时推送
- 🎨 **美化日志**: 使用 emoji 标识不同类型的操作和结果
- ⏰ **定时执行**: 每周日 UTC 时间 12:00 自动运行

## 🚀 快速开始

### 前置要求

1. **GitHub 账户**: 用于运行 GitHub Actions
2. **EUserv 账户**: 需要续期的服务器账户
3. **TrueCaptcha 账户**: 用于验证码识别（充值 $1 可识别约 3000 次）
4. **Mailparser 账户**: 用于解析邮箱中的 PIN 码
5. **Telegram Bot**: 用于接收通知（可选）

### 配置步骤

#### 1. Fork 本项目

点击右上角 Fork 按钮，将本项目复制到你的 GitHub 账户。

#### 2. 配置 GitHub Secrets

进入你的仓库，点击 `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`，添加以下密钥：

| 密钥名称 | 说明 | 示例 |
|---------|------|------|
| `EUSERV_USERNAME` | EUserv 用户名/邮箱，多个账户用空格分隔 | `user1@email.com user2@email.com` |
| `EUSERV_PASSWORD` | EUserv 密码，多个密码用空格分隔 | `password1 password2` |
| `TRUECAPTCHA_USERID` | TrueCaptcha 用户ID | `your_userid` |
| `TRUECAPTCHA_APIKEY` | TrueCaptcha API密钥 | `your_apikey` |
| `MAILPARSER_DOWNLOAD_URL_ID` | Mailparser 下载URL ID，多个用空格分隔 | `id1 id2` |
| `TG_BOT_TOKEN` | Telegram Bot Token（可选） | `123456:ABC-DEF...` |
| `TG_USER_ID` | Telegram 用户ID（可选） | `123456789` |

#### 3. 启用 GitHub Actions

进入 `Actions` 选项卡，点击 `I understand my workflows, go ahead and enable them` 启用工作流。

#### 4. 手动触发测试（可选）

进入 `Actions` -> `Auto EUserv` -> `Run workflow`，手动触发一次运行以测试配置是否正确。

## 📋 服务配置说明

### TrueCaptcha 配置

1. 访问 [TrueCaptcha](https://apitruecaptcha.org/) 注册账户
2. 充值 $1 美元（可识别约 3000 次验证码）
3. 获取 User ID 和 API Key
4. 将 User ID 和 API Key 添加到 GitHub Secrets

### Mailparser 配置

1. 访问 [Mailparser](https://mailparser.io/) 注册账户
2. 创建一个新的 Inbox，将 EUserv 的邮件转发到这个 Inbox
3. 设置解析规则，提取 PIN 码字段
4. 获取 Download URL ID（在 Data 页面的下载链接中）
5. 将 Download URL ID 添加到 GitHub Secrets

**注意**: 如果你有多个 EUserv 账户，需要为每个账户创建单独的 Mailparser Inbox。

### Telegram Bot 配置（可选）

1. 在 Telegram 中搜索 `@BotFather`
2. 发送 `/newbot` 创建新的 Bot
3. 获取 Bot Token
4. 搜索 `@userinfobot` 获取你的 User ID
5. 将 Bot Token 和 User ID 添加到 GitHub Secrets

## 🔧 本地运行

如果你想在本地测试脚本：

```bash
# 克隆仓库
git clone https://github.com/your-username/EUserv-extend.git
cd EUserv-extend

# 创建虚拟环境
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export EUSERV_USERNAME="your_username"
export EUSERV_PASSWORD="your_password"
export TRUECAPTCHA_USERID="your_userid"
export TRUECAPTCHA_APIKEY="your_apikey"
export MAILPARSER_DOWNLOAD_URL_ID="your_id"
export TG_BOT_TOKEN="your_token"  # 可选
export TG_USER_ID="your_user_id"  # 可选

# 运行脚本
python Github_Action.py
```

## 📊 工作流程

```
开始
  ↓
读取配置 (从环境变量)
  ↓
遍历每个账户
  ↓
登录 EUserv
  ├─ 需要验证码? → 调用 TrueCaptcha 识别
  └─ 登录成功
  ↓
获取服务器列表
  ↓
遍历每台服务器
  ├─ 可以续期?
  │   ↓
  │   触发安全检查 (发送 PIN 到邮箱)
  │   ↓
  │   等待 60 秒
  │   ↓
  │   从 Mailparser 获取 PIN
  │   ↓
  │   使用 PIN 获取 Token
  │   ↓
  │   提交续期请求
  │   ↓
  │   ✅ 续期成功
  └─ 不需要续期 → 跳过
  ↓
检查续期状态
  ↓
处理下一个账户
  ↓
发送 Telegram 通知
  ↓
结束
```

## 🎯 日志示例

```
🔑 [AutoEUServerless] 正在续费第 1 个账号
🧩 [Captcha Solver] 正在进行验证码识别...
🧩 [Captcha Solver] 识别的验证码是: 42
🧩 [Captcha Solver] 使用的是您自己的 apikey。
📊 [Captcha Solver] 当前日期 2024-01-01 API 使用次数: 5
✔️ [Captcha Solver] 验证通过
🌐 [AutoEUServerless] 检测到第 1 个账号有 2 台 VPS，正在尝试续期
🔗 [AutoEUServerless] ServerID: 1234567 已成功续订!
✅ [AutoEUServerless] ServerID: 7654321 无需更新
🏁 [AutoEUServerless] 所有工作完成！尽情享受~
```

## ⚙️ 高级配置

你可以在 `Github_Action.py` 中修改以下参数：

```python
# 最大登录重试次数
LOGIN_MAX_RETRY_COUNT = 1

# 接收 PIN 的等待时间，单位为秒
WAITING_TIME_OF_PIN = 60

# 是否检查验证码解决器的使用情况
CHECK_CAPTCHA_SOLVER_USAGE = True
```

## ❓ 常见问题

### Q: 为什么需要 Mailparser？

A: EUserv 的续期操作需要邮箱接收 PIN 码进行二次验证。Mailparser 可以自动解析邮件并提供 API 访问，使脚本能够自动获取 PIN 码。

### Q: TrueCaptcha 免费吗？

A: TrueCaptcha 不再提供免费试用，但充值 $1 可以识别约 3000 次验证码，对于个人使用已经非常充足。

### Q: 可以不使用 Telegram 通知吗？

A: 可以。如果不配置 `TG_BOT_TOKEN` 和 `TG_USER_ID`，脚本会跳过 Telegram 通知，但仍会在 GitHub Actions 的日志中显示运行结果。

### Q: 支持多少个账户？

A: 理论上没有限制，但要确保：
- 用户名、密码、Mailparser ID 的数量必须一致
- 用空格分隔多个值
- 每个账户需要独立的 Mailparser Inbox

### Q: 为什么续期失败？

A: 可能的原因：
1. 账户信息错误
2. 验证码识别失败（可能需要充值 TrueCaptcha）
3. Mailparser 配置错误或 PIN 码未及时获取
4. 网络问题
5. 服务器当前不可续期（时间未到）

请查看 GitHub Actions 的日志或 Telegram 通知了解具体错误信息。

## 📝 开发说明

### 项目结构

```
EUserv-extend/
├── .github/
│   └── workflows/
│       └── auto_euserv.yml      # GitHub Actions 工作流
├── .gitignore                    # Git 忽略文件
├── Github_Action.py              # 主脚本文件
├── requirements.txt              # Python 依赖
├── README.md                     # 英文文档
├── README_CN.md                  # 中文文档
└── PROJECT_ANALYSIS.md           # 项目分析报告
```

### 依赖说明

- `requests`: HTTP 请求库
- `beautifulsoup4`: HTML 解析库

### 贡献指南

欢迎提交 Issue 和 Pull Request！

## 📜 许可证

本项目基于 GPL-3.0-or-later 许可证开源。

## ⚠️ 免责声明

- 本项目仅供学习和个人使用
- 请遵守 EUserv 的服务条款
- 使用本脚本所产生的任何后果由使用者自行承担
- 请勿将本项目用于商业用途

## 🙏 致谢

- 感谢 [TrueCaptcha](https://apitruecaptcha.org/) 提供验证码识别服务
- 感谢 [Mailparser](https://mailparser.io/) 提供邮件解析服务
- 感谢所有贡献者和使用者

## 🔗 相关链接

- [EUserv Customer Panel](https://support.euserv.com)
- [TrueCaptcha API](https://apitruecaptcha.org/)
- [Mailparser](https://mailparser.io/)
- [Telegram Bot API](https://core.telegram.org/bots/api)

---

如有问题或建议，欢迎提交 Issue！
