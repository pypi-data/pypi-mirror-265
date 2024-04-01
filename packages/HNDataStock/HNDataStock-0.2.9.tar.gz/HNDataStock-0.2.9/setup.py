# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name='HNDataStock',
    version='0.2.9',
    author='Hướng Nghiệp Dữ Liệu',
    author_email='daotao@huongnghiepdulieu.com',
    description='Trường đào tạo lập trình Forex, Crypto, Chứng Khoán',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='http://www.huongnghiepdulieu.com',
    packages=find_packages(),
    install_requires=[
        'requests',
        'yfinance'
    ],
   classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: Vietnamese',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'License :: OSI Approved :: MIT License'
    ],
)
