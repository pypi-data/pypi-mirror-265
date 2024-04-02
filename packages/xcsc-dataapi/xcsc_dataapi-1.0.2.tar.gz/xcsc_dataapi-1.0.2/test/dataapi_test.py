# -*- coding:utf-8 -*-
"""
Created on 2024/3/28
@author: pei jian
"""
from xcsc_dataapi.data import token

from xcsc_dataapi.data.client import DataApi

if __name__ == "__main__":
    pro = token.pro_api('xxx')
    pro.query(api_url='/stk/api_fm_prd_indx_quot_sw')