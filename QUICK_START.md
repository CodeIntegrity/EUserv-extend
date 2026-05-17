# 🚀 快速开始指南

> 5分钟快速了解和部署 EUserv-extend 自动续期脚本

## 📌 这是什么？

一个自动续订 EUserv 免费服务器的 Python 脚本，通过 GitHub Actions 每周自动运行，无需人工干预。

## ✨ 核心功能

- ✅ 自动登录 EUserv
- ✅ 自动识别验证码
- ✅ 自动获取邮件 PIN 码
- ✅ 自动续订服务器合约
- ✅ Telegram 通知运行结果
- ✅ 支持多个账户

## 🎯 3步部署

### 1️⃣ Fork 项目

点击右上角 **Fork** 按钮

### 2️⃣ 添加 Secrets

进入你的仓库 → `Settings` → `Secrets and variables` → `Actions` → `New repository secret`

**必需配置**:
```
EUSERV_USERNAME          你的用户名（多个用空格分隔）
EUSERV_PASSWORD          你的密码（多个用空格分隔）
TRUECAPTCHA_USERID       TrueCaptcha用户ID
TRUECAPTCHA_APIKEY       TrueCaptcha API密钥
IMAP_HOST                IMAP服务器地址
IMAP_USERNAME            IMAP登录用户名
IMAP_PASSWORD            IMAP登录密码或应用专用密码
```

**可选配置**（推荐）:
```
TG_BOT_TOKEN            Telegram Bot Token
TG_USER_ID              Telegram 用户ID
```

### 3️⃣ 启用 Actions

进入 `Actions` 选项卡 → 点击 `I understand my workflows, go ahead and enable them`

✅ **完成！** 脚本将在每周日自动运行

## 🧩 服务申请

### TrueCaptcha（验证码识别）

1. 访问 https://apitruecaptcha.org/
2. 注册账户
3. 充值 $1（可识别 ~3000 次）
4. 获取 User ID 和 API Key

### IMAP 邮箱（PIN 码读取）

1. 确认接收 EUserv 邮件的邮箱已开启 IMAP
2. 如邮箱服务商要求，创建应用专用密码
3. 获取 IMAP 服务器地址
4. 配置 IMAP 用户名和密码

### Telegram Bot（可选，推荐）

1. 搜索 @BotFather
2. 发送 `/newbot` 创建 Bot
3. 获取 Token
4. 搜索 @userinfobot 获取你的 User ID

## 📝 配置示例

假设你有 2 个 EUserv 账户：

```bash
# 账户信息
EUSERV_USERNAME="user1@email.com user2@email.com"
EUSERV_PASSWORD="password1 password2"

# 多账户可共用一个 IMAP 邮箱，也可按账户用空格分隔
IMAP_HOST="imap.example.com"
IMAP_USERNAME="mail@example.com"
IMAP_PASSWORD="your_imap_or_app_password"

# TrueCaptcha 配置（所有账户共用）
TRUECAPTCHA_USERID="your_userid"
TRUECAPTCHA_APIKEY="your_apikey"

# Telegram 通知（可选）
TG_BOT_TOKEN="123456:ABC-DEF..."
TG_USER_ID="123456789"
```

⚠️ **注意**: 账户数量必须匹配！

## 🧪 测试运行

配置完成后：
1. 进入 `Actions` → `Auto EUserv`
2. 点击 `Run workflow` → `Run workflow`
3. 等待运行完成
4. 查看日志或 Telegram 消息

## 📚 更多文档

- 📖 [详细中文文档](README_CN.md) - 完整使用指南
- 🔍 [项目分析](PROJECT_ANALYSIS.md) - 代码深度分析
- 📊 [项目总结](PROJECT_SUMMARY.md) - 项目状态评估

## ❓ 常见问题

**Q: 为什么需要 TrueCaptcha？**  
A: 用于自动识别登录验证码

**Q: 为什么需要 IMAP 邮箱？**  
A: EUserv 续期需要邮件 PIN 码验证，脚本会通过 IMAP 自动读取本次触发后的 PIN 邮件

**Q: 可以不用 Telegram 吗？**  
A: 可以，不配置也能正常运行，但看不到通知

**Q: 支持几个账户？**  
A: 理论上无限制，但要确保配置数量一致

**Q: 为什么续期失败？**  
A: 检查配置是否正确、服务余额是否充足、查看详细日志

## 📞 获取帮助

- 查看 GitHub Actions 运行日志
- 查看 Telegram 通知消息
- 阅读完整文档 [README_CN.md](README_CN.md)
- 提交 Issue

---

**⏱️ 预计部署时间**: 15-30 分钟  
**💰 预计成本**: $1（TrueCaptcha，可选）+ 免费（IMAP 邮箱）  
**🔄 运行频率**: 每周日 UTC 12:00

祝你使用愉快！🎉
