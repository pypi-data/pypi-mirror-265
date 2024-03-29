# -*- coding:utf-8 -*-
"""
Created on 2024/3/28
@author: pei jian
"""
from gmssl.sm4 import CryptSM4, SM4_ENCRYPT, SM4_DECRYPT
import time
import requests
from xcsc_dataapi.util.sm4_cbc_util import encrypt_cbc

from xcsc_dataapi.data import client


def get_token(login_name='', secret_key='', key='', iv=''):
    """
        国密sm4解密
        :param login_name:账号（详见txt账号内容）
        :param secret_key:密钥（详见txt账号内容）
        :param key: sm4密钥（详见txt账号内容）
        :param iv: sm4偏移量（详见txt账号内容）
        :return: accessToken
        """
    if login_name == '' or login_name is None:
        raise Exception('获取令牌token失败：用户名不能为空')
    if secret_key == '' or secret_key is None:
        raise Exception('获取令牌token失败：密钥不能为空')
    if key == '' or key is None:
        raise Exception('获取令牌token失败：sm4 key不能为空')
    if iv == '' or iv is None:
        raise Exception('获取令牌token失败：sm4 iv不能为空')
    timestamp = round(time.time() * 1000)
    encrypt_str = bytes(login_name + "|" + secret_key + "|" + str(timestamp), "utf-8")
    crypt_sm4 = CryptSM4()

    # 加密
    # enc_cbc_value即为数据服务系统header里的Authorization的值
    enc_cbc_value = encrypt_cbc(crypt_sm4, key.encode('utf-8'), iv.encode('utf-8'), encrypt_str)
    init_url = 'https://dataapi.xcsc.com/data-api/init'  # 获取令牌accessToken URL
    init_data = {'data': {'loginName': login_name}}  # 数据

    init_headers = {
        'Content-Type': 'application/json',  # 自定义Content-Type头
        'Authorization': enc_cbc_value  # 自定义授权头
    }

    init_response = requests.post(init_url, json=init_data, headers=init_headers, verify=False)
    access_token_in = ''
    if init_response.status_code == 200:
        init_result = init_response.json()
        code = init_result['code']
        if code == '0':
            # access_token会有失效时间，请在有效期内使用，不要每次请求api都重新生成新的access_token!!!
            access_token_in = init_result['data']['accessToken']  # access_token
            print('获取令牌token成功, token=' + access_token_in)
        else:
            print('获取令牌token失败：' + init_result['msg'])

    else:
        Exception('初始化获取accessToken请求失败,'+init_response.text)

    return access_token_in


def pro_api(token=''):
    """
                Parameters
                ----------
                token: str
                    API接口TOKEN，用于用户认证
                """
    if token == '' or token is None:
        raise Exception('dataapi init error, token不能为空，请通过get_token获取')
    if token is not None and token != '':
        pro = client.DataApi(token)
        return pro
    else:
        raise Exception('dataapi init error')
