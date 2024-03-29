from setuptools import setup, find_packages
import codecs
import os


def read(fname):
    return codecs.open(os.path.join(os.path.dirname(__file__), fname)).read()


long_desc = """
XcscDataApi
===============

https://dataapi.xcsc.com/dss-frontend/login

"""


setup(
    name='xcsc_dataapi',
    version=read('xcsc_dataapi/VERSION.txt'),
    author="Xiangcai Security",
    author_email="itsupport@xcsc.com",
    description='xcsc_data data api',
    license='MIT',

    # 程序的详细描述
    long_description=long_desc,
    url='https://www.xcsc.com',
    keywords='Financial Data',

    # 程序的所属分类列表
    classifiers=[
        'Development Status :: 4 - Beta',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: MIT License'
    ],

    # 需要处理的包目录（包含__init__.py的文件夹）
    packages=find_packages(),

    #安装的依赖
    install_requires=[
        'requests',
        'gmssl',
        #'idna>=3.6',
        'certifi',
        #'pycryptodomex',
        'charset-normalizer'
    ],
    include_package_data=True,
    package_data={'': ['*.csv', '*.txt']},
)
