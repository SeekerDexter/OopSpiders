#!/usr/bin/env python3
# -*- coding:utf-8 -*-
from urllib.request import urlopen
from bs4 import BeautifulSoup
import random
import re
import datetime

pages = set()
random.seed(datetime.datetime.now())


def getInternalLinks(bsObj, includeUrl):
    """
    获取页面所有内链的列表
    :param bsObj: bs4(BeautifulSoup)对象
    :param includeUrl: str，当前bsObj的域名
    :return: list
    """
    internalLinks = []
    # 找出所有以“/”开头的链接
    for link in bsObj.findAll('a', href=re.compile('^(/|.*'+includeUrl+')')):
        if link.attrs['href'] is not None:  # "attrs"是个字典，来自bs4的一类对象
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks


def getExternalLinks(bsObj, includeUrl):
    externalLinks = []
    # 找出所有以“http”或“www”开头且不包含当前url的链接。（我觉得正则写得不严谨）
    for link in bsObj.findAll('a', href=re.compile('^(http|https|www)((?!'+includeUrl+').)*$')):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks


def splitAddress(addr):
    """
    获取url的域名
    :param addr: 
    :return: 
    """
    addrParts = addr.replace('http://', '').split('/')
    return addrParts


def getRandomExternalLink(page):
    # 打开一个url
    html = urlopen(page)
    # 制作该页的bs4对象
    bsObj = BeautifulSoup(html)
    # 外链列表
    externalLinks = getExternalLinks(bsObj, splitAddress(page)[1])
    # 判断该页内是否有外链
    if len(externalLinks) == 0:
        # 没有，随机选择一个内链进入下一层继续寻找外链
        internalLinks = getInternalLinks(bsObj, splitAddress(page)[1])
        print(splitAddress(page))
        return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks)-1)])
    else:
        return externalLinks[random.randint(0, len(externalLinks)-1)]


def followExternalOnly(startingSite):
    externalLink = getRandomExternalLink(startingSite)
    print('随机外链为：'+externalLink)
    followExternalOnly(externalLink)

if __name__ == "__main__":
    followExternalOnly('https://www.baidu.com')