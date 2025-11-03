# LLM OCR 迁移指南

## 概述

本项目已从 TrueCaptcha API 迁移到使用 OpenAI GPT-4o-mini 的 OCR 能力进行验证码识别。这一改造使项目能够：

- 脱离 TrueCaptcha 的限制
- 使用更强大的 LLM 视觉能力进行验证码识别
- 提高识别准确率
- 支持更灵活的配置

## 主要变更

### 1. 依赖项更新

新增以下依赖项（已更新到 `requirements.txt`）：
- `openai>=1.0.0` - OpenAI Python SDK
- `Pillow>=10.0.0` - 图像处理库

### 2. 环境变量变更

**移除的环境变量：**
- `TRUECAPTCHA_USERID`
- `TRUECAPTCHA_APIKEY`

**新增的环境变量：**
- `OPENAI_API_KEY` - OpenAI API 密钥（必需）
- `OPENAI_MODEL` - 使用的模型名称（可选，默认：`gpt-4o-mini`）

### 3. 配置说明

在 GitHub Actions Secrets 中配置以下环境变量：

```yaml
OPENAI_API_KEY: your-openai-api-key-here
OPENAI_MODEL: gpt-4o-mini  # 可选，默认使用 gpt-4o-mini
```

如果需要使用其他支持视觉能力的模型，可以设置 `OPENAI_MODEL` 为：
- `gpt-4o-mini` （推荐，成本较低）
- `gpt-4o`
- `gpt-4-turbo`
- 其他支持 vision 的模型

### 4. 代码改造细节

#### 新增函数：
- `resize_image()` - 图像缩放，减少 API 传输量
- `encode_image_to_base64()` - 将图像编码为 base64
- `invoke_llm_ocr()` - 调用 OpenAI Vision API 进行 OCR

#### 修改的函数：
- `captcha_solver()` - 改用 LLM OCR 进行验证码识别
- `handle_captcha_solved_result()` - 简化结果处理逻辑，支持直接返回计算结果
- `log()` - 更新 emoji 映射，`[Captcha Solver]` 改为 `[LLM OCR]`

#### 移除的函数：
- `get_captcha_solver_usage()` - 不再需要检查 TrueCaptcha 使用情况

### 5. OCR 配置参数

在代码中可以调整以下参数：

```python
OCR_MAX_RETRIES = 3          # OCR API 调用最大重试次数
OCR_RETRY_DELAY = 2          # OCR 重试延迟（秒）
OCR_IMAGE_MAX_SIZE = (300, 100)  # OCR 图片缩放最大尺寸
```

## 使用说明

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

创建 `.env` 文件或在系统中设置环境变量：

```bash
export OPENAI_API_KEY="your-openai-api-key"
export EUSERV_USERNAME="your-username"
export EUSERV_PASSWORD="your-password"
export MAILPARSER_DOWNLOAD_URL_ID="your-mailparser-id"
```

### 3. 运行脚本

```bash
python Github_Action.py
```

## 成本估算

使用 GPT-4o-mini 的成本非常低：
- 输入：$0.15 / 1M tokens
- 输出：$0.60 / 1M tokens

每次验证码识别大约消耗：
- 图像 token（约 85-255 tokens，取决于图像大小）
- 输出 token（约 10-50 tokens）

估算每次识别成本约 $0.0001-0.0003（约 0.0007-0.002 元人民币），远低于 TrueCaptcha 的成本。

## 优势

1. **更高的准确率** - LLM 视觉能力强大，能更准确识别验证码
2. **更低的成本** - GPT-4o-mini 成本低廉
3. **更灵活** - 可以通过调整 prompt 来优化识别效果
4. **无需额外服务** - 只需要 OpenAI API Key
5. **可扩展性强** - 支持更复杂的验证码类型

## 故障排查

### 问题：API 调用失败

**解决方案：**
1. 检查 `OPENAI_API_KEY` 是否正确设置
2. 确认 API Key 有足够的额度
3. 检查网络连接是否正常
4. 查看日志中的错误信息

### 问题：验证码识别不准确

**解决方案：**
1. 调整 `invoke_llm_ocr()` 函数中的 prompt
2. 增加重试次数 `OCR_MAX_RETRIES`
3. 尝试使用更强大的模型（如 `gpt-4o`）

### 问题：图像过大导致处理慢

**解决方案：**
1. 调整 `OCR_IMAGE_MAX_SIZE` 参数，使用更小的尺寸
2. 优化图像压缩质量

## 技术细节

### Prompt 设计

当前使用的 prompt 针对 EUserv 的数学算式验证码进行了优化：

```
请对这张验证码图片进行OCR识别。这是一个简单的数学算式验证码，可能包含加法(+)、减法(-)或乘法(X/x)运算。请直接输出算式结果的数字，不要输出其他内容。
```

如果遇到不同类型的验证码，可以修改这个 prompt 以获得更好的效果。

### 图像预处理

1. 使用 Pillow 对图像进行缩放（默认最大 300x100）
2. 转换为 PNG 格式
3. Base64 编码后发送给 API

这些预处理步骤可以：
- 减少 API 传输时间
- 降低 token 消耗
- 提高处理速度

## 贡献

如果你有任何改进建议或发现问题，欢迎提交 Issue 或 Pull Request。
