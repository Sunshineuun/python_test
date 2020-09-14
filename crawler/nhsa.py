#!/usr/bin/env python
# encoding: utf-8
# qiushengming
import csv
import json

from bs4 import BeautifulSoup
from selenium import webdriver

from crawler.utils import create_chrome_web_driver
from utils.excel_utils import WriteXLSXCustom

"""
说明
2020年9月7日
国家医保局药品目录爬网（8月份更新）
网址：http://code.nhsa.gov.cn:8000/search.html?sysflag=100
数据请求：http://code.nhsa.gov.cn:8000/yp/getPublishGoodsDataInfo.html?
数据请求参数：

    companyNameSc=&
    registeredProductName=&
    approvalCode=&
    batchNumber=20200826&
    _search=false&
    nd=1599447997476&
    rows=100&
    page=2&
    sidx=t.goods_code&
    sord=asc

mitmproxy使用参考
https://www.cnblogs.com/lsdb/p/10106655.html
https://www.cnblogs.com/grandlulu/p/9525417.html

mitmproxy启动命令：mitmweb -s "C:\\Users\\qiushengming\\PycharmProjects\\test\\crawler\\mitmproxy\\addons.py"
浏览器启动命令："C:\Program Files (x86)\Google\Chrome\Application\chrome.exe" --proxy-server=127.0.0.1:8080 --ignore-certificate-errors
"""


def start():
    # 定义URL列表
    base_url = 'http://code.nhsa.gov.cn:8000/yp/getPublishGoodsDataInfo.html?companyNameSc=&registeredProductName=&approvalCode=&batchNumber=20200826&_search=false&nd=1599447997476&rows=100&page={page}&sidx=t.goods_code&sord=asc'
    url_list = []
    for i in range(1, 938):
        url_list.append(base_url.format(page=i))

    keys = [
        "goodscode",
        "registeredproductname",
        "goodsname",
        "registeredmedicinemodel",
        "registeredoutlook",
        "materialname",
        "factor",
        "minunit",
        "unit",
        "companynamesc",
        "approvalcode",
        "goodsstandardcode",
        "productinsurancetype",
        "productcode",
        "productname",
        "productmedicinemodel",
        "productremark"
    ]

    # 用selenium发送请求
    driver = create_chrome_web_driver()

    # 将请求结果写入到txt文件
    json_file = open('D:\\Temp\\nhsa.txt', 'w', encoding='utf-8')
    # 将结构化的数据写入
    row_file = open('D:\\Temp\\nhsa.csv', 'w', encoding='utf-8')
    csv_writer = csv.writer(row_file)
    for url in url_list:
        driver.get(url=url)

        # 或者网页源码
        page_source = driver.page_source
        # 转换
        soup = BeautifulSoup(page_source, 'html.parser')
        # 获取正文
        text = soup.find('body').text
        # 存储json
        json_file.write(text)
        # 转换为json格式
        _json = json.loads(text)
        # 从json中获取每行数据
        temp_rows = []
        for row in _json['rows']:
            temp_row = []
            for k in keys:
                if k in row:
                    temp_row.append(str(row[k]).replace('\n', ''))
                else:
                    temp_row.append('')
            temp_rows.append(temp_row)
        csv_writer.writerows(temp_rows)
    # f.close()
    # driver.close()
    # 写入Excel
    pass


if __name__ == '__main__':
    start()
