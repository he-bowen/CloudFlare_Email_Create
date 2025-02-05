import json
import os
import requests

# 配置文件路径
CONFIG_FILE = "config.json"

def load_config():
    """加载配置文件"""
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(f"配置文件 {CONFIG_FILE} 不存在")
    
    with open(CONFIG_FILE, "r") as f:
        return json.load(f)

def create_email(zone_id, email, forward_to, api_key, account_email):
    """创建单个邮箱"""
    url = f"https://api.cloudflare.com/client/v4/zones/{zone_id}/email/routing/rules"
    
    headers = {
        "X-Auth-Email": account_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    data = {
        "name": f"Forward {email}",
        "enabled": True,
        "matchers": [{
            "type": "literal",
            "field": "to",
            "value": email
        }],
        "actions": [{
            "type": "forward",
            "value": [forward_to]
        }]
    }
    
    print(f"请求URL: {url}")
    print(f"请求头: {{'X-Auth-Email': '{headers['X-Auth-Email']}', 'X-Auth-Key': '***{api_key[-4:]}'}}")
    print(f"请求数据: {data}")
    
    response = requests.post(url, headers=headers, json=data, timeout=10)
    
    try:
        return response.json()
    except json.JSONDecodeError:
        print(f"API返回无效JSON，状态码：{response.status_code}")
        print(f"原始响应内容：{response.text[:200]}")  # 打印前200个字符
        return {"success": False, "errors": [{"message": "Invalid API response"}]}

def verify_api_key(api_key, account_email):
    """验证API Key有效性"""
    url = "https://api.cloudflare.com/client/v4/user/tokens/verify"
    headers = {
        "X-Auth-Email": account_email,
        "X-Auth-Key": api_key,
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=5)
        result = response.json()
        # 修改验证逻辑
        if response.status_code == 200 and result.get("success"):
            return True
        return False
    except Exception as e:
        print(f"验证API Key时出错: {str(e)}")
        return False

def main():
    try:
        # 加载配置
        config = load_config()
        
        # 获取配置项
        zone_id = config.get("zone_id")
        api_key = config.get("api_key")
        emails = config.get("emails")
        account_email = config.get("account_email")
        
        if not zone_id or not api_key or not emails:
            raise ValueError("配置文件中缺少必要参数")
        
        # 仅保留网络检查
        try:
            test_response = requests.get("https://api.cloudflare.com", timeout=5)
            print("网络连接测试通过")
        except Exception as e:
            print(f"网络连接失败: {str(e)}")
            exit()
        
        # 批量创建邮箱
        for email_config in emails:
            email = email_config.get("email")
            forward_to = email_config.get("forward_to")
            
            if not email or not forward_to:
                print(f"跳过无效配置: {email_config}")
                continue
            
            result = create_email(zone_id, email, forward_to, api_key, account_email)
            
            if result.get("success"):
                print(f"成功创建邮箱: {email} -> {forward_to}")
            else:
                print(f"创建邮箱失败: {email}")
                print(result.get("errors"))
                
    except Exception as e:
        print(f"程序运行出错: {str(e)}")

if __name__ == "__main__":
    main()
