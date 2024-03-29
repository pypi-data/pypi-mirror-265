# -*- coding:utf-8 -*-
"""
Created on 2024/3/29
@author: pei jian
"""
import binascii

from gmssl.sm4 import SM4_ENCRYPT, SM4_DECRYPT


def str_to_hex_str(hex_str):
    """
    字符串转hex
    :param hex_str: 字符串
    :return: hex
    """
    hex_data = hex_str.encode('utf-8')
    str_bin = binascii.unhexlify(hex_data)
    return str_bin.decode('utf-8')


def encrypt_cbc(crypt_sm4, encrypt_key, encrypt_iv, value):
    """
    国密sm4加密
    :param crypt_sm4:
    :param encrypt_key: sm4加密key
    :param encrypt_iv: sm4加密iv
    :param value: 待加密的字符串
    :return: sm4加密后的hex值
    """
    crypt_sm4.set_key(encrypt_key, SM4_ENCRYPT)
    encrypt_value = crypt_sm4.crypt_cbc(encrypt_iv, value)
    return encrypt_value.hex()


def decryptCBC(crypt_sm4, decrypt_key, decrypt_iv, encrypt_value):
    """
    国密sm4解密
    :param crypt_sm4:
    :param decrypt_key:sm4加密key
    :param decrypt_iv:sm4加密iv
    :param encrypt_value: 待解密的hex值
    :return: 原字符串
    """
    crypt_sm4.set_key(decrypt_key, SM4_DECRYPT)
    decrypt_value = crypt_sm4.crypt_cbc(decrypt_iv, bytes.fromhex(encrypt_value))  # bytes类型
    return str_to_hex_str(decrypt_value.hex())