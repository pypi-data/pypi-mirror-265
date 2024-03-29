# -*- coding:utf-8 -*-
"""
Created on 2024/3/28
@author: pei jian
"""
import time
from functools import partial

import requests


class DataApi:
    __token = ''
    __http_url = 'https://dataapi.xcsc.com/data-api'

    def __init__(self, token, timeout=10):
        self.__token = token
        self.__timeout = timeout

    def query(self, api_url='', fields='', current_page='', data_type='', **kwargs):
        """
                    查询数据
                    :param api_url:接口地址，不包含域名及上下文
                    :param current_page: 当前页数，不传默认是 1
                    :param fields: 上送字段列表
                    :param data_type: 返回数据类型，不传默认是 dataframe格式,支持json和dataframe
                    :return: api data
                    """
        if self.__token == '':
            return "token值未填"
        api_headers = {
            'Content-Type': 'application/json',  # 自定义Content-Type头
            'Authorization': self.__token  # init 接口获取到的access_token
        }
        data_dict = kwargs
        # 向字典中添加新的键值对
        data_dict["currentPage"] = current_page  # 当前页数，1 代表第一页，2 代表第二页
        data_dict["fieldList"] = fields  # 自定义返回相应参数，不传或者为空默认都是返回全部，传参内容以逗号【,】分割
        api_data = {
            'requestId': time.time_ns(),
            'data': data_dict
        }
        response = requests.post(self.__http_url + api_url, json=api_data, headers=api_headers, verify=False,
                                 timeout=self.__timeout)
        if response.status_code == 200:
            print('api接口请求成功')
            print(response.text)
        else:
            print('api接口请求失败,' + response.text)

        return response.text

    def __getattr__(self, name):
        return partial(self.query, name)
