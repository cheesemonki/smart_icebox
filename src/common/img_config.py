import requests
import base64

# 获取Token
def get_token(username, password, domainname, project_name):
    url = "https://iam.cn-north-4.myhuaweicloud.com/v3/auth/tokens"
    headers = {"Content-Type": "application/json"}
    body = {
        "auth": {
            "identity": {
                "methods": ["password"],
                "password": {
                    "user": {
                        "name": username,
                        "password": password,
                        "domain": {"name": domainname}
                    }
                }
            },
            "scope": {"project": {"name": project_name}}
        }
    }
    response = requests.post(url, json=body, headers=headers)
    return response.headers["X-Subject-Token"]

# 获取对象数据
def get_object_data(token, bucket_name, object_name):
    url = f"https://{bucket_name}.obs.cn-north-4.myhuaweicloud.com/{object_name}"
    headers = {
        "Authorization": f"OBS {token}",
        "Date": "current_date"  # 替换为当前日期
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.content
    else:
        raise Exception(f"Failed to get object data: {response.status_code}")

# 图像标签识别
def image_tagging(token, base64_image):
    url = "https://image.cn-north-4.myhuaweicloud.com/v2.0/image/tagging"
    headers = {
        "X-Auth-Token": token,
        "Content-Type": "application/json"
    }
    body = {"image": base64_image}
    response = requests.post(url, json=body, headers=headers)
    return response.json()

# 主程序
def main():
    username = "your_username"
    password = "your_password"
    domainname = "your_domainname"
    project_name = "cn-north-4"
    bucket_name = "examplebucket"  # 替换为你的桶名
    object_name = "path_to_your_image.jpg"  # 替换为你的对象名
    
    # 获取Token
    token = get_token(username, password, domainname, project_name)
    
    # 获取图像数据
    image_data = get_object_data(token, bucket_name, object_name)
    
    # 图像编码
    base64_image = base64.b64encode(image_data).decode("utf-8")
    
    # 获取图像标签
    result = image_tagging(token, base64_image)
    print(result)

if __name__ == "__main__":
    main()
