# coding: utf-8
import requests

import base64
from huaweicloudsdkcore.auth.credentials import BasicCredentials
from huaweicloudsdkcore.exceptions import exceptions
from huaweicloudsdkcore.http.http_config import HttpConfig
from huaweicloudsdkimage.v2 import ImageClient,RunImageTaggingRequest,ImageTaggingReq
from huaweicloudsdkimage.v2.region.image_region import ImageRegion

if __name__ == "__main__":
    # 从环境变量中获取AK和SK
    # ak = os.getenv["GBPLAMSYPUIDMYEM653J"]
    # sk = os.getenv["HmscL5gAkm60iuXNFwqaPDENMvvBy2wkPlFQ1jZ6"]
    ak = "GBPLAMSYPUIDMYEM653J"
    sk = "HmscL5gAkm60iuXNFwqaPDENMvvBy2wkPlFQ1jZ6"


    # 创建认证对象
    credentials = BasicCredentials(ak, sk)

    # 构建客户端
    client = ImageClient.new_builder() \
        .with_credentials(credentials) \
        .with_region(ImageRegion.value_of("cn-north-4")) \
        .build()



    # 图片URL
    image_url = "https://pic.616pic.com/ys_bnew_img/00/04/57/6BmvM9DuAl.jpg"

    # 选择上传方式：URL或base64
    upload_method = "url"  # 可以改为 "base64" 来使用base64上传方式

    if upload_method == "url":
        # 使用URL上传
        image_tagging_req = ImageTaggingReq()
        image_tagging_req.url = image_url

    elif upload_method == "base64":
        # 使用base64上传本地图片
        with open("./resource/image-tagging.jpg", "rb") as image_file:
            file_data = image_file.read()
        file_base64_str = base64.b64encode(file_data).decode('utf-8')
        image_tagging_req = ImageTaggingReq()
        image_tagging_req.image = file_base64_str

    # 构建请求
    request = RunImageTaggingRequest()
    request.body = image_tagging_req

    try:
        # 发送请求
        response = client.run_image_tagging(request)
        print(response)
        response_json = response.to_json_object()  # 将响应转换为JSON对象

        # 准备要发送的GET请求的URL和参数
        target_url = "http://example.com/your-endpoint"  # 替换为实际的URL
        params = response_json  # 将响应JSON作为查询参数

        # 发送GET请求
        result = requests.get(target_url, params=params)

        # 打印结果
        print(result.text)

    except exceptions.ClientRequestException as e:
        print("Status Code:", e.status_code)
        print("Request ID:", e.request_id)
        print("Error Code:", e.error_code)
        print("Error Message:", e.error_msg)