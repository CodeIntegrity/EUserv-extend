# EUserv-extend 自动续期脚本

[English](README.md) | 简体中文

## 📖 项目简介

这是一个基于 Python 3 的自动化脚本，用于自动续订 EUserv 服务器合约。该脚本通过 GitHub Actions 定时执行，无需手动干预即可完成续期操作。

### 主要特性

- ✅ **自动登录**: 自动处理 EUserv 客户面板登录
- 🧩 **双模式验证码识别**: 支持 TrueCaptcha API 和 LLM OCR 两种验证码识别方式
- 🔧 **灵活配置**: 支持自定义 OpenAI base_url，兼容各种 OpenAI API 服务
- 📧 **PIN 码获取**: 通过 IMAP 直连邮箱获取安全 PIN 码
- 🔄 **自动续期**: 自动检测并续订即将到期的服务器合约
- 👥 **多账户支持**: 支持批量处理多个 EUserv 账户
- 📱 **Telegram 通知**: 运行结果通过 Telegram Bot 实时推送
- 🎨 **美化日志**: 使用 emoji 标识不同类型的操作和结果
- ⏰ **定时执行**: 每周日 UTC 时间 12:00 自动运行

## 🚀 快速开始

### 前置要求

1. **GitHub 账户**: 用于运行 GitHub Actions
2. **EUserv 账户**: 需要续期的服务器账户
3. **验证码识别服务**（二选一）:
   - **LLM OCR**: OpenAI API Key（推荐，成本极低，默认方式）
   - **TrueCaptcha**: TrueCaptcha 账户（传统方式）
4. **可 IMAP 登录的邮箱**: 用于接收并读取 EUserv 安全 PIN 码（默认方式）
5. **Telegram Bot**: 用于接收通知（可选）

### 配置步骤

#### 1. Fork 本项目

点击右上角 Fork 按钮，将本项目复制到你的 GitHub 账户。

#### 2. 配置 GitHub Secrets

进入你的仓库，点击 `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`，添加以下密钥：

| 密钥名称 | 必需 | 说明 | 示例 |
|---------|------|------|------|
| `EUSERV_USERNAME` | 是 | EUserv 用户名/邮箱，多个账户用空格分隔 | `user1@email.com user2@email.com` |
| `EUSERV_PASSWORD` | 是 | EUserv 密码，多个密码用空格分隔 | `password1 password2` |
| `CAPTCHA_SOLVER_TYPE` | 否 | 验证码识别方式：`truecaptcha` 或 `llm`（默认） | `llm` |
| `TRUECAPTCHA_USERID` | 条件 | TrueCaptcha 用户ID（使用 TrueCaptcha 时必需） | `your_userid` |
| `TRUECAPTCHA_APIKEY` | 条件 | TrueCaptcha API密钥（使用 TrueCaptcha 时必需） | `your_apikey` |
| `OPENAI_API_KEY` | 条件 | OpenAI API 密钥（使用 LLM OCR 时必需） | `sk-...` |
| `OPENAI_BASE_URL` | 否 | 自定义 OpenAI API 端点（可选） | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 否 | OpenAI 模型名称（可选，默认 gpt-4o-mini） | `gpt-4o-mini` |
| `IMAP_HOST` | 是 | IMAP 服务器地址，可单值共享或按账户空格分隔 | `imap.example.com` |
| `IMAP_PORT` | 否 | IMAP 端口，默认 `993` | `993` |
| `IMAP_USERNAME` | 是 | IMAP 登录用户名，可单值共享或按账户空格分隔 | `mail@example.com` |
| `IMAP_PASSWORD` | 是 | IMAP 登录密码或应用专用密码，可单值共享或按账户空格分隔 | `app_password` |
| `IMAP_MAILBOX` | 否 | 邮箱目录，默认 `INBOX`，可单值共享或按账户空格分隔 | `INBOX` |
| `IMAP_USE_SSL` | 否 | 是否使用 SSL，默认 `true` | `true` |
| `IMAP_SEARCH_CRITERIA` | 否 | IMAP 搜索条件，默认 `(FROM "euserv")` | `(FROM "euserv")` |
| `IMAP_PIN_MAX_RETRIES` | 否 | IMAP 获取 PIN 最大重试次数，默认 `6` | `6` |
| `IMAP_PIN_RETRY_DELAY` | 否 | IMAP 获取 PIN 重试间隔秒数，默认 `30` | `30` |
| `IMAP_LOOKBACK_LIMIT` | 否 | 在搜索结果中回看最近多少封邮件，默认 `20` | `20` |
| `TG_BOT_TOKEN` | 否 | Telegram Bot Token（可选） | `123456:ABC-DEF...` |
| `TG_USER_ID` | 否 | Telegram 用户ID（可选） | `123456789` |

#### 3. 启用 GitHub Actions

进入 `Actions` 选项卡，点击 `I understand my workflows, go ahead and enable them` 启用工作流。

#### 4. 手动触发测试（可选）

进入 `Actions` -> `Auto EUserv` -> `Run workflow`，手动触发一次运行以测试配置是否正确。

## 📋 验证码识别服务配置

### 方式一：LLM OCR（推荐，默认）

#### 基本配置
1. 访问 [OpenAI Platform](https://platform.openai.com/) 注册账户
2. 在 [API Keys](https://platform.openai.com/api-keys) 页面创建新的 API Key
3. 将 API Key 添加到 GitHub Secrets（`OPENAI_API_KEY`）
4. 无需设置 `CAPTCHA_SOLVER_TYPE`（默认为 `llm`）

#### 高级配置：自定义 Base URL
如果你的网络环境无法直接访问 OpenAI API，或想使用兼容 OpenAI API 的其他服务：

**使用场景**：
- Azure OpenAI Service
- 第三方中转服务
- 自部署的兼容服务
- Cloudflare AI Gateway

**配置方法**：
```bash
# 设置自定义端点
OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
```

**成本说明**：
- GPT-4o-mini：输入 $0.15/1M tokens，输出 $0.60/1M tokens
- 每次验证码识别消耗约 85-255 tokens（输入）+ 10-50 tokens（输出）
- 每次成本约 $0.0001-0.0003（约 0.0007-0.002 元人民币）

### 方式二：TrueCaptcha（传统方式）

1. 访问 [TrueCaptcha](https://apitruecaptcha.org/) 注册账户
2. 充值 $1 美元（可识别约 3000 次验证码）
3. 获取 User ID 和 API Key
4. 添加到 GitHub Secrets：
   - `CAPTCHA_SOLVER_TYPE=truecaptcha`
   - `TRUECAPTCHA_USERID`
   - `TRUECAPTCHA_APIKEY`

**成本说明**：
- $1 识别约 3000 次
- 每次成本约 $0.00033

### 对比总结

| 特性 | LLM OCR | TrueCaptcha |
|------|---------|-------------|
| 准确率 | ⭐⭐⭐⭐⭐ 更高 | ⭐⭐⭐⭐ 较高 |
| 成本 | $0.0001-0.0003/次 | $0.00033/次 |
| 配置难度 | 简单 | 简单 |
| 自定义端点 | ✅ 支持 | ❌ 不支持 |
| 推荐度 | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |

## 📧 PIN 获取配置

### IMAP 直连邮箱

脚本会在触发 EUserv 安全检查后等待 PIN 邮件送达，然后使用 Python 标准库通过 IMAP 登录邮箱，读取本次触发后收到的 EUserv 邮件并提取 6 位 PIN。无需第三方邮件解析服务，也不会新增第三方依赖。

1. 确认接收 EUserv 邮件的邮箱已开启 IMAP。
2. 如果邮箱服务商要求应用专用密码，请创建应用专用密码。
3. 在 GitHub Actions 中配置：
   - `IMAP_HOST`
   - `IMAP_USERNAME`
   - `IMAP_PASSWORD`
4. 可按需配置 `IMAP_PORT`、`IMAP_MAILBOX`、`IMAP_SEARCH_CRITERIA` 等变量。

**多账户说明**: `IMAP_HOST`、`IMAP_USERNAME`、`IMAP_PASSWORD`、`IMAP_MAILBOX` 支持单值共享，也支持与 `EUSERV_USERNAME` 一样用空格分隔逐账户配置。多个 EUserv 账户共用同一个收件邮箱时只填一个 IMAP 配置即可。

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

# 安装 uv（如本机尚未安装，请参考 https://docs.astral.sh/uv/）
# 本项目使用 uv 管理 Python 运行方式，不建议全局 pip 安装依赖

# 设置环境变量（使用 LLM OCR）
export EUSERV_USERNAME="your_username"
export EUSERV_PASSWORD="your_password"
export CAPTCHA_SOLVER_TYPE="llm"  # 可选，默认为 llm
export OPENAI_API_KEY="sk-your-api-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 可选，自定义端点
export OPENAI_MODEL="gpt-4o-mini"  # 可选，默认为 gpt-4o-mini
export IMAP_HOST="imap.example.com"
export IMAP_USERNAME="mail@example.com"
export IMAP_PASSWORD="your_imap_or_app_password"
export IMAP_MAILBOX="INBOX"  # 可选，默认为 INBOX
export TG_BOT_TOKEN="your_token"  # 可选
export TG_USER_ID="your_user_id"  # 可选

# 或使用 TrueCaptcha
# export CAPTCHA_SOLVER_TYPE="truecaptcha"
# export TRUECAPTCHA_USERID="your_userid"
# export TRUECAPTCHA_APIKEY="your_apikey"

# 运行脚本
uv run --with-requirements requirements.txt python Github_Action.py
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
  ├─ 需要验证码? → 根据配置调用 TrueCaptcha 或 LLM OCR 识别
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
  │   从 IMAP 获取 PIN
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

### 使用 LLM OCR
```
🔑 [AutoEUServerless] 正在续费第 1 个账号
🧩 [Captcha Solver] 使用 LLM OCR 进行验证码识别...
🧩 [LLM OCR] 识别的验证码是: 42
✔️ [Captcha Solver] 验证通过
🌐 [AutoEUServerless] 检测到第 1 个账号有 2 台 VPS，正在尝试续期
🔗 [AutoEUServerless] ServerID: 1234567 已成功续订!
✅ [AutoEUServerless] ServerID: 7654321 无需更新
🏁 [AutoEUServerless] 所有工作完成！尽情享受~
```

### 使用 TrueCaptcha
```
🔑 [AutoEUServerless] 正在续费第 1 个账号
🧩 [Captcha Solver] 使用 TrueCaptcha 进行验证码识别...
🧩 [TrueCaptcha] 使用的是您自己的 apikey。
🧩 [TrueCaptcha] 识别的验证码是: 42
📊 [TrueCaptcha] 当前日期 2024-01-01 API 使用次数: 5
✔️ [Captcha Solver] 验证通过
🌐 [AutoEUServerless] 检测到第 1 个账号有 2 台 VPS，正在尝试续期
🔗 [AutoEUServerless] ServerID: 1234567 已成功续订!
✅ [AutoEUServerless] ServerID: 7654321 无需更新
🏁 [AutoEUServerless] 所有工作完成！尽情享受~
```

## ⚙️ 高级配置

你可以在 `Github_Action.py` 中修改以下参数：

```python
# 验证码识别方式
CAPTCHA_SOLVER_TYPE = 'llm'  # 'truecaptcha' 或 'llm'

# 最大登录重试次数
LOGIN_MAX_RETRY_COUNT = 1

# 接收 PIN 的等待时间，单位为秒
WAITING_TIME_OF_PIN = 60

# LLM OCR 配置
OCR_MAX_RETRIES = 3          # OCR API 调用最大重试次数
OCR_RETRY_DELAY = 2          # OCR 重试延迟（秒）
OCR_IMAGE_MAX_SIZE = (300, 100)  # OCR 图片缩放最大尺寸

# TrueCaptcha 使用情况检查
CHECK_CAPTCHA_SOLVER_USAGE = True  # 是否检查 TrueCaptcha API 使用次数
```

## ❓ 常见问题

### Q: 应该选择 TrueCaptcha 还是 LLM OCR？

A: **推荐使用 LLM OCR**（默认）：
- ✅ 识别准确率更高
- ✅ 成本更低（$0.0001-0.0003/次）
- ✅ 支持自定义端点（解决网络访问问题）
- ✅ 无需额外注册第三方服务

如果你已有 TrueCaptcha 账户和余额，也可以继续使用。

### Q: 网络无法访问 OpenAI API 怎么办？

A: 可以使用 `OPENAI_BASE_URL` 配置自定义端点：
- 使用第三方中转服务
- 使用 Azure OpenAI Service
- 使用 Cloudflare AI Gateway
- 详见 [双模式配置指南](DUAL_MODE_GUIDE.md)

### Q: LLM OCR 成本高吗？

A: 非常低廉。使用 gpt-4o-mini 模型，每次验证码识别成本约 $0.0001-0.0003（约 0.0007-0.002 元人民币），与 TrueCaptcha 相当或更低。

### Q: 可以不使用 Telegram 通知吗？

A: 可以。如果不配置 `TG_BOT_TOKEN` 和 `TG_USER_ID`，脚本会跳过 Telegram 通知，但仍会在 GitHub Actions 的日志中显示运行结果。

### Q: 支持多少个账户？

A: 理论上没有限制，但要确保：
- 用户名、密码数量必须一致
- IMAP 配置可以单值共享，也可以用空格分隔后与账户数量一致

### Q: 为什么续期失败？

A: 可能的原因：
1. 账户信息错误
2. 验证码识别失败
   - LLM OCR：API Key 无效、额度不足、网络问题
   - TrueCaptcha：余额不足、网络问题
3. IMAP 配置错误、邮箱未开启 IMAP、搜索条件不匹配，或 PIN 码未及时获取
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
- `openai`: OpenAI Python SDK
- `Pillow`: 图像处理库

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

- 感谢 [OpenAI](https://openai.com/) 提供强大的 LLM OCR 能力
- 感谢 [TrueCaptcha](https://apitruecaptcha.org/) 提供传统验证码识别服务
- 感谢所有贡献者和使用者

## 🔗 相关链接

- [EUserv Customer Panel](https://support.euserv.com)
- [OpenAI Platform](https://platform.openai.com/)
- [TrueCaptcha API](https://apitruecaptcha.org/)
- [Telegram Bot API](https://core.telegram.org/bots/api)
- [双模式配置指南](DUAL_MODE_GUIDE.md) - 详细的验证码识别配置说明
- [LLM OCR 迁移指南](LLM_OCR_MIGRATION.md) - 从 TrueCaptcha 迁移到 LLM OCR

---

如有问题或建议，欢迎提交 Issue！
