#!/usr/bin/env python
# encoding: utf-8
# qiushengming-minnie

"""
说明
2020年9月8日
国药监药品目录爬网
网址：https://www.nmpa.gov.cn/yaopin/index.html
爬网需求描述及爬网字段见附件
"""
import json
import logging
import random
import time

import os

from bs4 import BeautifulSoup
from selenium import webdriver
import pyautogui

"""
1. Python的编码规范
PackageNotFoundError: Packages missing in current channels:

  - mitmproxy
"""
"""
关于selenium定位的常用方法
1.id定位：find_element_by_id(self, id_)
2.name定位：find_element_by_name(self, name)
3.class定位：find_element_by_class_name(self, name)
4.tag定位：find_element_by_tag_name(self, name)
5.link定位：find_element_by_link_text(self, link_text)
6.partial_link定位find_element_by_partial_link_text(self, link_text)
7.xpath定位：find_element_by_xpath(self, xpath)
8.css定位：find_element_by_css_selector(self, css_selector)
"""
"""
moveTo(x，y)将鼠标移动到指定的 x、y 坐标。
moveRel (xOffset，yOffset)相对于当前位置移动鼠标。
dragTo(x，y)按下左键移动鼠标。
dragRel (xOffset，yOffset)按下左键，相对于当前位置移动鼠标。
click(x，y，button)模拟点击(默认是左键)。
rightClick() 模拟右键点击。
middleClick() 模拟中键点击。
doubleClick() 模拟左键双击。
mouseDown(x，y，button)模拟在 x、y 处按下指定鼠标按键。
mouseUp(x，y，button)模拟在 x、y 处释放指定键。
scroll(units)模拟滚动滚轮。正参数表示向上滚动，负参数表示向下滚动。
typewrite(message)键入给定消息字符串中的字符。
typewrite([key1，key2，key3])键入给定键字符串。
press(key)按下并释放给定键。
keyDown(key)模拟按下给定键。
keyUp(key)模拟释放给定键。
hotkey([key1，key2，key3])模拟按顺序按下给定键字符串，然后以相反的顺序释放。
screenshot() 返回屏幕快照的 Image 对象(参见第 17 章关于 Image 对象的信息)。
"""
"""
mitmporxy下载经历
1. 更新pip的版本
    python -m pip install -U pip
2. 使用国内镜像
    pip install browsermobproxy -i http://pypi.douban.com/simple/ --trusted-host pypi.douban.com
--trusted-host pypi.douban.com 这是为了获得ssl证书的认证
"""
"""
<table width="2000" height="200" border="0" cellspacing="0" cellpadding="0">
"""
"""
http://app1.nmpa.gov.cn/data_nmpa/face3/base.jsp?tableId=25&tableName=TABLE25&title=%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81&bcId=152904713761213296322795806604&CbSlDlH0=qArmqqrFK2NFK2NFKbJzH8B2eTrzIDkCDF0r06WuES0qqmL
"""
# 分割线，pyautogui属性定义------------------------------------------------------
pyautogui.PAUSE = 1  # 每个函数执行后停顿1.5秒
pyautogui.FAILSAFE = True  # 鼠标移到左上角会触发FailSafeException，因此快速移动鼠标到左上角也可以停止
# 分割线，属性定义---------------------------------------------------------------
# CFDA-国产药品主页地址
cfda_cn_drug_home_page = \
    'http://qy1.sfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=25&tableName=TABLE25&title=%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81&bcId=152904713761213296322795806604http://qy1.sfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=25&tableName=TABLE25&title=%E5%9B%BD%E4%BA%A7%E8%8D%AF%E5%93%81&bcId=152904713761213296322795806604'
# CFDA-进口药品主页地址
cfda_en_drug_home_page = \
    'http://qy1.sfda.gov.cn/datasearchcnda/face3/base.jsp?tableId=36&tableName=TABLE36&title=%E8%BF%9B%E5%8F%A3%E8%8D%AF%E5%93%81&bcId=152904858822343032639340277073'

duration = 1  # 鼠标移动的持续时间


# 分割线，url请求拦截定义---------------------------------------------------------------


# 分割线，函数定义---------------------------------------------------------------
def sleep_time():
    return random.randint(5, 7)


def dir_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def read_config():
    with open("D:/Temp/config.txt", "r") as f:
        config_str = f.read()
    print(config_str)
    config = json.loads(config_str)
    return config


def click(x, y):
    """
    点击，并判断是否响应成功，如果响应不成功返回Fasel，响应成功返回True
    :param x:
    :param y:
    :return:
    """
    pyautogui.moveTo(x, y, duration=duration)
    pyautogui.click()  # 点击它一下

    while True:
        """
        循环读取，如果未结束
        """
        time.sleep(sleep_time())
        _config = read_config()
        if _config['is_request_end'] == '1':
            """
            是否请求结束，1表示结束，0表示未结束
            """
            if _config['response_status_code'] == 200:
                """
                是否响应成功，200表示成功；非200都表示失败。
                """
                return True
            else:
                return False


def enter_main_page():
    pyautogui.scroll(2000)  # 置顶
    while True:
        if click(280, 450):
            break
    pyautogui.scroll(-2000)  # 置底


def jump_to_page(_config):
    while True:
        # 回到首页
        enter_main_page()

        # 定位到页面输入栏
        pyautogui.moveTo(1480, 800, duration=1)
        pyautogui.click()
        pyautogui.doubleClick()

        # 输入页码
        pyautogui.typewrite(_config['curstart'])
        if click(1570, 800):
            return


def page_handle(_page):
    """
    对于单页的操作
    注意：
    1. 第一条数据的坐标位，和偏移位至关重要。
    :param: page
    :return:
    """
    # 截图，按照页去存储;左侧，顶部，宽度和高度
    config = read_config()
    print("目前正在采集第{}页".format(config['curstart']))
    date = time.strftime("%Y%m%d%H", time.localtime())
    _dir = "D:/Temp/CFDA/{}".format(date)
    dir_exists(_dir)
    file_path = "{}/{}_Page.png".format(_dir, config['curstart'])
    pyautogui.screenshot(file_path, region=(0, 0, 1920, 1080))

    # x, y = 123, 281  # 第一条记录的的坐标 国产
    x, y = 525, 193  # 第一条记录的的坐标 进口；123, 281
    x_return, y_return = 1647, 220  # 返回按钮的坐标 1582, 325；1648,202；1670, 150
    x_next, y_next = 1240, 800  # 下一页按钮的坐标 1250

    start_index = config['index']
    # 暂停
    # time.sleep(sleep_time())
    # 循环点击界面中的15条记录
    for i in range(1, 16):
        if i >= start_index:
            # 暂停
            time.sleep(sleep_time())

            is_ok = click(x, y)  # 点击，进行详情页

            if not is_ok:
                # 返回首页
                return False

            time.sleep(sleep_time())
            is_ok = click(x_return, y_return)  # 点击，返回按钮

            if not is_ok:
                # 返回首页
                return False

        y += 39  # 每行数据x坐标差35

    # 下一页
    pyautogui.moveTo(x_next, y_next, duration=duration)
    pyautogui.click()
    return True


def to_soup(html):
    """
    返回BeautifulSoup对象，详细使用见API
    http://beautifulsoup.readthedocs.io/zh_CN/v4.4.0/ \n
    :param html: 带有html标签的字符串 \n
    :return: BeautifulSoup对象 \n
    """
    return BeautifulSoup(html, 'html.parser')


if __name__ == '__main__':
    """
    测试用机器的像素是：1920,1080
    driver = None
      WARNING: The scripts mitmdump.exe, mitmproxy.exe, mitmweb.exe, pathoc.exe and pathod.exe
       are installed in 'd:\program files\python36\Scripts' which is not on PATH.
  Consider adding this directory to PATH or, 
  if you prefer to suppress this warning, use --no-warn-script-location.
    """

    print('程序开始执行')
    # time.sleep(2)
    # 刷新界面
    # pyautogui.press('f5')

    # point = pyautogui.position()
    # print("鼠标所在坐标点：", point)

    # pyautogui.hotkey('ctrl', 'Home')  # 置顶操作
    # pyautogui.moveTo(x=1592, y=76, duration=2)  # 将鼠标移动到指定位置，该方法是偏移位置而不是坐标点
    # pyautogui.scroll(1000)  # 下滚到指定位置，让界面上的记录暴露出来

    # 1032,1908;在浏览器最大化时候滚动条(下拉)的坐标
    # pyautogui.moveTo(x=1592, y=835, duration=2)  # 将鼠标移动到指定位置，该方法是偏移位置而不是坐标点
    # pyautogui.scroll(-497)  # 下滚到指定位置，让界面上的记录暴露出来 [国产.-250,进口.-500]

    #  1450,995; 点击翻页输入框
    # page = '22'
    # pyautogui.moveTo(x=1400, y=1000, duration=2)
    # pyautogui.doubleClick()
    # pyautogui.typewrite(page, 0.25)
    #
    # time.sleep(random.randint(1, 10))

    #  1530,985; 点击go按钮
    # pyautogui.moveTo(x=1500, y=985, duration=2)
    # pyautogui.click()

    time.sleep(5)
    pyautogui.click(70, 230)
    # 跳转到某页面
    jump_to_page(read_config())
    for page in range(1, 11042):
        is_ok1 = page_handle(page)
        if not is_ok1:
            jump_to_page(read_config())
            pass
