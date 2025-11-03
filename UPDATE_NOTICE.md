# 🎉 项目更新通知

## 新版本特性

### ✨ 双模式验证码识别
现在支持**两种验证码识别方式**，您可以根据需求自由选择：

#### 🔹 方式一：LLM OCR（推荐，默认）
- 基于 OpenAI GPT-4o-mini 的视觉识别
- 识别准确率更高
- 成本更低（$0.0001-0.0003/次）
- **支持自定义 base_url**（重要！）

#### 🔹 方式二：TrueCaptcha（传统方式）
- 保留原有的 TrueCaptcha API 支持
- 适合已有 TrueCaptcha 账户的用户

### 🌟 核心亮点：支持自定义 OpenAI Base URL

这是本次更新最重要的功能！通过配置 `OPENAI_BASE_URL`，您可以：

✅ **解决网络访问问题**
- 使用第三方中转服务
- 使用国内镜像服务

✅ **使用企业级服务**
- Azure OpenAI Service
- Cloudflare AI Gateway

✅ **完全私有化部署**
- 自部署的兼容模型（vLLM、Xinference 等）
- 完全掌控数据安全

## 快速开始

### 继续使用 TrueCaptcha（无需改动）

如果您已经配置了 TrueCaptcha，只需添加一个环境变量：

```bash
CAPTCHA_SOLVER_TYPE=truecaptcha
```

其他配置保持不变，脚本会继续使用 TrueCaptcha。

### 切换到 LLM OCR（推荐）

#### 基础配置（可直接访问 OpenAI）
```bash
# 只需配置 API Key，其他都是默认值
OPENAI_API_KEY=sk-your-key
```

#### 高级配置（使用自定义端点）
```bash
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://your-endpoint.com/v1  # 关键！
OPENAI_MODEL=gpt-4o-mini  # 可选
```

## GitHub Actions 配置

### 添加新的 Secrets

进入 `Settings` -> `Secrets and variables` -> `Actions`，添加：

| Secret 名称 | 必需 | 说明 |
|------------|------|------|
| `CAPTCHA_SOLVER_TYPE` | 否 | `truecaptcha` 或 `llm`（默认 `llm`） |
| `OPENAI_API_KEY` | 使用 LLM 时必需 | OpenAI API 密钥 |
| `OPENAI_BASE_URL` | 否 | 自定义 API 端点 |
| `OPENAI_MODEL` | 否 | 模型名称（默认 `gpt-4o-mini`） |

**注意**：保留原有的 `TRUECAPTCHA_*` secrets，以便随时切换回来。

## 使用场景示例

### 场景 1：直接使用官方 OpenAI
```bash
OPENAI_API_KEY=sk-xxx
# 默认使用 LLM OCR，无需其他配置
```

### 场景 2：使用中转服务（解决网络问题）
```bash
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://api.your-proxy.com/v1
```

### 场景 3：使用 Azure OpenAI
```bash
OPENAI_API_KEY=your-azure-key
OPENAI_BASE_URL=https://your-resource.openai.azure.com/openai/deployments/your-deployment
OPENAI_MODEL=gpt-4o
```

### 场景 4：继续使用 TrueCaptcha
```bash
CAPTCHA_SOLVER_TYPE=truecaptcha
TRUECAPTCHA_USERID=your-userid
TRUECAPTCHA_APIKEY=your-apikey
```

## 配置建议

### 推荐配置（新用户）
```bash
# 最简配置，使用 LLM OCR
EUSERV_USERNAME=user@email.com
EUSERV_PASSWORD=your-password
OPENAI_API_KEY=sk-your-key
MAILPARSER_DOWNLOAD_URL_ID=your-id
```

### 推荐配置（网络受限）
```bash
# 使用自定义端点
EUSERV_USERNAME=user@email.com
EUSERV_PASSWORD=your-password
OPENAI_API_KEY=your-key
OPENAI_BASE_URL=https://your-endpoint.com/v1  # 关键配置
MAILPARSER_DOWNLOAD_URL_ID=your-id
```

### 双保险配置（推荐）
```bash
# 同时配置两种方式，随时切换
CAPTCHA_SOLVER_TYPE=llm  # 或 truecaptcha

# LLM OCR 配置
OPENAI_API_KEY=sk-xxx
OPENAI_BASE_URL=https://your-endpoint.com/v1  # 可选

# TrueCaptcha 配置（作为备用）
TRUECAPTCHA_USERID=your-userid
TRUECAPTCHA_APIKEY=your-apikey
```

## 成本对比

| 方式 | 成本 | 优势 |
|------|------|------|
| LLM OCR | $0.0001-0.0003/次 | 准确率高、支持自定义端点 |
| TrueCaptcha | $0.00033/次 | 传统方式、稳定可靠 |

## 详细文档

- 📖 [双模式配置指南](DUAL_MODE_GUIDE.md) - 完整的配置说明
- 📖 [双模式实现总结](DUAL_MODE_SUMMARY.md) - 技术细节
- 📖 [中文文档](README_CN.md) - 更新后的完整文档

## 常见问题

### Q: 我需要修改原有配置吗？
A: 不需要。如果您使用 TrueCaptcha，只需添加 `CAPTCHA_SOLVER_TYPE=truecaptcha` 即可。

### Q: 网络无法访问 OpenAI 怎么办？
A: 配置 `OPENAI_BASE_URL` 使用中转服务或其他兼容 OpenAI API 的服务。

### Q: 如何切换识别方式？
A: 只需修改 `CAPTCHA_SOLVER_TYPE` 环境变量即可，无需修改代码。

### Q: 两种方式可以同时配置吗？
A: 可以！推荐同时配置，通过 `CAPTCHA_SOLVER_TYPE` 控制使用哪一种，方便快速切换。

### Q: 默认使用哪种方式？
A: 默认使用 LLM OCR（如果不设置 `CAPTCHA_SOLVER_TYPE`）。

## 升级步骤

1. **拉取最新代码**
   ```bash
   git pull origin main
   ```

2. **选择识别方式**
   - 使用 LLM OCR：配置 `OPENAI_API_KEY`
   - 继续使用 TrueCaptcha：设置 `CAPTCHA_SOLVER_TYPE=truecaptcha`

3. **（可选）配置自定义端点**
   ```bash
   OPENAI_BASE_URL=https://your-endpoint.com/v1
   ```

4. **测试运行**
   - 手动触发 GitHub Actions workflow
   - 检查日志确认使用的识别方式

## 技术支持

如有问题，欢迎：
- 📖 查看 [双模式配置指南](DUAL_MODE_GUIDE.md)
- 💬 提交 GitHub Issue
- 📧 联系维护者

---

**祝您使用愉快！** 🎉

**双模式支持** ✅ | **Base URL 自定义** ✅ | **灵活切换** ✅
