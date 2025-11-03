# 双模式验证码识别配置指南

## 概述

本项目现在支持**两种验证码识别方式**：
1. **TrueCaptcha API** - 传统的验证码识别服务
2. **LLM OCR** - 基于 OpenAI GPT-4o-mini 的视觉识别能力

你可以通过配置环境变量来选择使用哪种方式。

## 快速选择

### 推荐使用 LLM OCR
- ✅ 识别准确率更高
- ✅ 成本更低（每次 $0.0001-0.0003）
- ✅ 支持自定义 base_url（兼容 OpenAI API 的服务）
- ✅ 无需额外注册第三方服务

### 继续使用 TrueCaptcha
- ✅ 已有 TrueCaptcha 账户和余额
- ✅ 不想使用 OpenAI 服务
- ✅ 网络环境无法访问 OpenAI API

## 配置方式

### 方式一：使用 LLM OCR（默认，推荐）

#### 环境变量配置

```bash
# 验证码识别方式（可选，默认为 llm）
CAPTCHA_SOLVER_TYPE=llm

# OpenAI API 配置（必需）
OPENAI_API_KEY=sk-your-api-key-here

# OpenAI Base URL（可选，用于兼容 OpenAI API 的服务）
OPENAI_BASE_URL=https://api.openai.com/v1  # 官方 API
# 或者使用其他兼容服务，例如：
# OPENAI_BASE_URL=https://your-custom-endpoint.com/v1

# OpenAI 模型（可选，默认 gpt-4o-mini）
OPENAI_MODEL=gpt-4o-mini
```

#### GitHub Actions Secrets 设置

| Secret 名称 | 必需 | 说明 | 示例 |
|------------|------|------|------|
| `CAPTCHA_SOLVER_TYPE` | 否 | 验证码识别方式 | `llm` |
| `OPENAI_API_KEY` | 是 | OpenAI API 密钥 | `sk-...` |
| `OPENAI_BASE_URL` | 否 | 自定义 API 端点 | `https://api.openai.com/v1` |
| `OPENAI_MODEL` | 否 | 使用的模型 | `gpt-4o-mini` |

### 方式二：使用 TrueCaptcha

#### 环境变量配置

```bash
# 验证码识别方式（必需）
CAPTCHA_SOLVER_TYPE=truecaptcha

# TrueCaptcha API 配置（必需）
TRUECAPTCHA_USERID=your-userid
TRUECAPTCHA_APIKEY=your-apikey
```

#### GitHub Actions Secrets 设置

| Secret 名称 | 必需 | 说明 | 示例 |
|------------|------|------|------|
| `CAPTCHA_SOLVER_TYPE` | 是 | 验证码识别方式 | `truecaptcha` |
| `TRUECAPTCHA_USERID` | 是 | TrueCaptcha 用户 ID | `your-userid` |
| `TRUECAPTCHA_APIKEY` | 是 | TrueCaptcha API Key | `your-apikey` |

## OpenAI Base URL 使用场景

### 1. 使用官方 OpenAI API
```bash
# 默认情况，无需设置 OPENAI_BASE_URL
OPENAI_API_KEY=sk-your-key
```

### 2. 使用 Azure OpenAI
```bash
OPENAI_API_KEY=your-azure-key
OPENAI_BASE_URL=https://your-resource-name.openai.azure.com/openai/deployments/your-deployment-name
OPENAI_MODEL=gpt-4o  # Azure 部署名称
```

### 3. 使用自部署的兼容服务
```bash
OPENAI_API_KEY=your-custom-key
OPENAI_BASE_URL=https://your-self-hosted-service.com/v1
OPENAI_MODEL=gpt-4o-mini
```

### 4. 使用第三方 OpenAI 兼容服务
```bash
# 例如使用国内的中转服务
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://your-proxy-service.com/v1
OPENAI_MODEL=gpt-4o-mini
```

## 成本对比

### TrueCaptcha
- 充值 $1 可识别约 3000 次
- 每次成本：约 $0.00033
- 需要预先充值

### LLM OCR (GPT-4o-mini)
- 按使用量计费
- 输入：$0.15/1M tokens
- 输出：$0.60/1M tokens
- 每次成本：约 $0.0001-0.0003
- 无需预充值

**结论**：LLM OCR 成本略低且更灵活。

## 完整配置示例

### 示例 1：使用 LLM OCR（官方 OpenAI）

```bash
# GitHub Actions Secrets
EUSERV_USERNAME=user@example.com
EUSERV_PASSWORD=your-password
CAPTCHA_SOLVER_TYPE=llm  # 可选，默认就是 llm
OPENAI_API_KEY=sk-your-openai-key
MAILPARSER_DOWNLOAD_URL_ID=your-id
TG_BOT_TOKEN=your-telegram-token  # 可选
TG_USER_ID=your-telegram-id  # 可选
```

### 示例 2：使用 LLM OCR（自定义端点）

```bash
# GitHub Actions Secrets
EUSERV_USERNAME=user@example.com
EUSERV_PASSWORD=your-password
CAPTCHA_SOLVER_TYPE=llm
OPENAI_API_KEY=your-custom-key
OPENAI_BASE_URL=https://your-custom-endpoint.com/v1
OPENAI_MODEL=gpt-4o-mini
MAILPARSER_DOWNLOAD_URL_ID=your-id
TG_BOT_TOKEN=your-telegram-token  # 可选
TG_USER_ID=your-telegram-id  # 可选
```

### 示例 3：使用 TrueCaptcha

```bash
# GitHub Actions Secrets
EUSERV_USERNAME=user@example.com
EUSERV_PASSWORD=your-password
CAPTCHA_SOLVER_TYPE=truecaptcha
TRUECAPTCHA_USERID=your-userid
TRUECAPTCHA_APIKEY=your-apikey
MAILPARSER_DOWNLOAD_URL_ID=your-id
TG_BOT_TOKEN=your-telegram-token  # 可选
TG_USER_ID=your-telegram-id  # 可选
```

## 本地运行配置

### 使用 LLM OCR

```bash
# 克隆项目
git clone https://github.com/your-username/EUserv-extend.git
cd EUserv-extend

# 安装依赖
pip install -r requirements.txt

# 设置环境变量
export EUSERV_USERNAME="your_username"
export EUSERV_PASSWORD="your_password"
export CAPTCHA_SOLVER_TYPE="llm"  # 可选
export OPENAI_API_KEY="sk-your-key"
export OPENAI_BASE_URL="https://api.openai.com/v1"  # 可选
export OPENAI_MODEL="gpt-4o-mini"  # 可选
export MAILPARSER_DOWNLOAD_URL_ID="your_id"
export TG_BOT_TOKEN="your_token"  # 可选
export TG_USER_ID="your_user_id"  # 可选

# 运行脚本
python Github_Action.py
```

### 使用 TrueCaptcha

```bash
# 设置环境变量
export EUSERV_USERNAME="your_username"
export EUSERV_PASSWORD="your_password"
export CAPTCHA_SOLVER_TYPE="truecaptcha"
export TRUECAPTCHA_USERID="your_userid"
export TRUECAPTCHA_APIKEY="your_apikey"
export MAILPARSER_DOWNLOAD_URL_ID="your_id"
export TG_BOT_TOKEN="your_token"  # 可选
export TG_USER_ID="your_user_id"  # 可选

# 运行脚本
python Github_Action.py
```

## 故障排查

### 问题 1：未设置验证码识别方式

**错误信息**：
```
不支持的验证码识别方式: xxx
```

**解决方案**：
- 检查 `CAPTCHA_SOLVER_TYPE` 是否设置为 `truecaptcha` 或 `llm`
- 如果未设置，默认使用 `llm` 方式

### 问题 2：LLM OCR 缺少 API Key

**错误信息**：
```
使用 LLM OCR 需要设置 OPENAI_API_KEY
```

**解决方案**：
- 确保设置了 `OPENAI_API_KEY` 环境变量
- 检查 API Key 是否有效

### 问题 3：TrueCaptcha 缺少配置

**错误信息**：
```
使用 TrueCaptcha 需要设置 TRUECAPTCHA_USERID 和 TRUECAPTCHA_APIKEY
```

**解决方案**：
- 确保设置了 `TRUECAPTCHA_USERID` 和 `TRUECAPTCHA_APIKEY`
- 检查 TrueCaptcha 账户是否有足够余额

### 问题 4：自定义 Base URL 连接失败

**错误信息**：
```
Connection error or timeout
```

**解决方案**：
- 检查 `OPENAI_BASE_URL` 是否正确
- 确保网络可以访问该端点
- 验证 API Key 是否与该端点匹配

## 日志输出

### LLM OCR 模式
```
🧩 [Captcha Solver] 使用 LLM OCR 进行验证码识别...
🧩 [LLM OCR] 使用自定义 base_url: https://custom.com/v1  # 如果配置了
🧩 [LLM OCR] 识别的验证码是: 42
✔️ [Captcha Solver] 验证通过
```

### TrueCaptcha 模式
```
🧩 [Captcha Solver] 使用 TrueCaptcha 进行验证码识别...
🧩 [TrueCaptcha] 使用的是您自己的 apikey。
🧩 [TrueCaptcha] 识别的验证码是: 42
📊 [TrueCaptcha] 当前日期 2024-01-01 API 使用次数: 5
✔️ [Captcha Solver] 验证通过
```

## 迁移指南

### 从 TrueCaptcha 迁移到 LLM OCR

1. 获取 OpenAI API Key
2. 更新 GitHub Secrets：
   - 设置 `CAPTCHA_SOLVER_TYPE=llm`（或删除此项，使用默认值）
   - 设置 `OPENAI_API_KEY`
   - 可选：设置 `OPENAI_BASE_URL` 和 `OPENAI_MODEL`
3. 保留原有的 `TRUECAPTCHA_*` secrets（以便随时切换回来）
4. 手动触发一次 workflow 测试

### 从 LLM OCR 切换到 TrueCaptcha

1. 更新 GitHub Secrets：
   - 设置 `CAPTCHA_SOLVER_TYPE=truecaptcha`
   - 确保 `TRUECAPTCHA_USERID` 和 `TRUECAPTCHA_APIKEY` 已设置
2. 保留原有的 `OPENAI_*` secrets（以便随时切换回来）
3. 手动触发一次 workflow 测试

## 最佳实践

1. **推荐默认使用 LLM OCR**：成本低、准确率高、维护简单
2. **保留两套配置**：在 GitHub Secrets 中同时配置两种方式，便于快速切换
3. **监控使用情况**：
   - LLM OCR：在 OpenAI Dashboard 查看使用量
   - TrueCaptcha：日志会显示每日使用次数
4. **测试验证**：配置修改后先手动触发 workflow 测试
5. **自定义端点**：如果网络受限，使用 `OPENAI_BASE_URL` 配置中转服务

## 支持的 OpenAI 兼容服务

以下服务都兼容 OpenAI API 格式，可以通过设置 `OPENAI_BASE_URL` 使用：

1. **官方 OpenAI API** - https://api.openai.com/v1
2. **Azure OpenAI Service** - 企业级服务
3. **Cloudflare AI Gateway** - CDN 加速
4. **各种第三方中转服务** - 解决网络访问问题
5. **自部署的模型服务**（如 vLLM、Xinference）- 完全私有化

## 技术说明

- 两种模式的核心逻辑完全独立，互不影响
- 通过 `CAPTCHA_SOLVER_TYPE` 环境变量动态选择
- 支持运行时切换，无需修改代码
- 兼容性良好，支持各种 OpenAI API 兼容服务

## 贡献与反馈

如有问题或建议，欢迎提交 Issue 或 Pull Request！

---

**双模式支持** ✅ | **灵活配置** ✅ | **易于切换** ✅
