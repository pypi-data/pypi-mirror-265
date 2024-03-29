# -*- coding:utf-8 -*-
"""
Created on 2024/3/28
@author: pei jian
"""
from xcsc_dataapi.data import token

from xcsc_dataapi.data.client import DataApi

if __name__ == "__main__":
    pro = token.pro_api('662047fae69c4ef9acd35565bfc347e5')
    pro.query(api_url='/stk/api_fm_prd_indx_quot_sw', start_time='2023-01-01', end_time='2024-03-01', name='peij', fields='', current_page=1, data_type='dataframe')