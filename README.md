# Cloudflare邮箱批量创建

![Python版本](https://img.shields.io/badge/Python-3.6%2B-blue)
![依赖项](https://img.shields.io/badge/依赖项-requests-green)

该工具用于通过Cloudflare API批量创建邮件转发规则，实现自动化的邮箱地址转发配置。

## 功能特性

- 批量创建邮件转发规则
- 配置文件管理
- API密钥有效性验证
- 网络连接检查
- 详细的请求日志输出

## 安装步骤

1. 确保已安装Python 3.6+环境
2. 安装依赖库：
```bash
pip install requests
```

3. 克隆仓库或下载脚本文件：
```bash
git clone https://github.com/zopenb/CloudFlare_Email_Create.git
```

## 配置说明

在项目根目录创建 `config.json` 文件：

```json
{
    "zone_id": "your_zone_id",
    "api_key": "your_api_key",
    "account_email": "your_account@example.com",
    "emails": [
        {
            "email": "hello@yourdomain.com",
            "forward_to": "yourpersonal@email.com"
        },
        {
            "email": "support@yourdomain.com",
            "forward_to": "team@company.com"
        }
    ]
}
```

### 参数说明
- `zone_id`: Cloudflare区域ID（在域名概览页获取）
- `api_key`: Cloudflare API密钥（[获取地址](https://dash.cloudflare.com/profile/api-tokens)）
- `account_email`: Cloudflare账户邮箱
- `emails`: 邮箱配置数组
  - `email`: 需要创建的邮箱地址
  - `forward_to`: 邮件转发目标地址

## 使用方法

运行脚本：
```bash
python setup_emails.py
```

成功输出示例：
```
成功创建邮箱: hello@yourdomain.com -> yourpersonal@email.com
成功创建邮箱: support@yourdomain.com -> team@company.com
```

## 注意事项

1. **API权限要求**：
   - 需要具有`Zone.EmailRouting:edit`权限的API密钥
   - 确保域名已启用Email Routing功能

2. **网络要求**：
   - 确保可以访问Cloudflare API（api.cloudflare.com）

3. **安全警告**：
   - 不要将配置文件提交到版本库
   - 建议为API密钥设置IP白名单

4. **错误处理**：
   - 遇到错误时会显示具体原因
   - 常见错误代码：
     - 400: 请求参数错误
     - 403: API权限不足
     - 429: API请求次数过多

## 开发说明

### 调试模式
设置环境变量查看完整请求信息：
```bash
export DEBUG_MODE=1 && python setup_emails.py
```

### 测试覆盖率
包含以下测试场景：
- 配置文件验证
- API密钥验证
- 网络连接测试
- 邮件规则创建流程

## 贡献指南
欢迎提交Pull Request。重大更改请先创建Issue讨论。

## 许可证
[MIT License](LICENSE) © 2023 zopenb
