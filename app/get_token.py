import os
import json
from dotenv import load_dotenv
from aliyunsdkcore.client import AcsClient
from aliyunsdkcore.request import CommonRequest
load_dotenv()


def get_aliyun_token():
    # 创建AcsClient实例
    client = AcsClient(
        os.getenv('ALIYUN_AK_ID'),
        os.getenv('ALIYUN_AK_SECRET'),
        "cn-shanghai"
    )

    # 创建request，并设置参数。
    request = CommonRequest()
    request.set_method('POST')
    request.set_domain('nls-meta.cn-shanghai.aliyuncs.com')
    request.set_version('2019-02-28')
    request.set_action_name('CreateToken')

    try:
        response = client.do_action_with_exception(request)
        jss = json.loads(response)
        if 'Token' in jss and 'Id' in jss['Token']:
            t = jss['Token']['Id']
            et = jss['Token']['ExpireTime']
            return t, et
    except Exception as e:
        print(e)


# 按装订区域中的绿色按钮以运行脚本。
if __name__ == '__main__':
    token, expire_time = get_aliyun_token()
    print(token)
    print(expire_time)
