# -*- coding:utf-8 -*-
import codecs
import os

__version__ = codecs.open(os.path.join(os.path.dirname(__file__), 'VERSION.txt')).read()
__author__ = 'pei jian'

from xcsc_dataapi.data.token import (get_token, pro_api)



