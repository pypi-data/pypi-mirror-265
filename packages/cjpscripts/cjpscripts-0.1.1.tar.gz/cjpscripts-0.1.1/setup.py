#!/usr/bin/env python
# -*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: Cai Jianping
# Mail: jpingcai@163.com
# Created Time:  2022-7-9 11:25:34 AM
#############################################


from setuptools import setup, find_packages

setup(
    name="cjpscripts",
    version="0.1.1",
    keywords=("database", "localServer"),
    description="My Personal Script",
    long_description="My Personal Toolkit",
    license="MIT Licence",
    author="Cai Jianping",
    author_email="jpingcai@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=[]
)
