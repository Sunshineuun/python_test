#!/usr/bin/env python
# encoding: utf-8
# qiushengming-minnie
import datetime
import json
import logging
import os
import time
import mitmproxy
from mitmproxy import ctx

k1 = ['http://app1.nmpa.gov.cn/data_nmpa/face3/content.jsp?',  # 具体内容
      'http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?',  # 翻页
      'http://app1.nmpa.gov.cn/data_nmpa/face3/content.jsp?',
      'http://app1.nmpa.gov.cn/data_nmpa/face3/search.jsp?',
      ]
config_file_path = 'D:/Temp/config.txt'
cfda_xq_dir = 'D:/Temp/CFDA_2/CFDA-XQ'
cfda_page_dir = 'D:/Temp/CFDA_2/CFDA-PAGE'


def dir_exists(directory):
    if not os.path.exists(directory):
        os.mkdir(directory)


def parser_data(query):
    data = {}
    for key, value in query.items():
        data[key] = value
    return data


def update_config(params):
    with open(config_file_path, "r") as f:
        config_str = f.read()
    config = json.loads(config_str)
    config.update(params)
    with open(config_file_path, 'w', encoding='utf-8') as f:
        f.write(json.dumps(config))  # 存储爬到哪里，结构第几页,第几行
    return config


class Counter:
    def __init__(self):
        self.num = 0
        self.page_config = {}

    def request(self, flow: mitmproxy.http.HTTPFlow):
        self.num = self.num + 1
        ctx.log.info("We've seen %d flows" % self.num)
        # ctx.log.info()
        params = {
            'is_request_end': '0'
        }
        url = flow.request.url
        for k in k1:
            if str(url).startswith(k):
                self.page_config.update(update_config(params))
                print(self.page_config, 'request')
                break


def response(self, flow: mitmproxy.http.HTTPFlow):
    """
    (Called when) 来自服务端端的 HTTP 响应被成功完整读取。
    :param flow:
    :return:
    """

    print(self.page_config, 'response')
    url = flow.request.url
    # 判断请求是否是自己想要的url content
    if str(url).startswith(k1[0]) \
            or str(url).startswith(k1[2]):
        # 这个是每条的详情
        # params.update(parser_data(flow.request.query))

        self.page_config['DIR'] = '{}/第{}页'.format(cfda_xq_dir,
                                                   self.page_config.get('curstart'))

        self.page_config['file_name'] = '{}_{}.html'.format(
            self.page_config['tableName'],
            self.page_config['index']
        )
        self.page_config['index'] += 1
        self.page_config['index2'] += 1

    elif str(url).startswith(k1[1]) \
            or str(url).startswith(k1[3]):
        # search
        # print(parser_data(flow.request.urlencoded_form))
        # 这个是翻页
        self.page_config.update(parser_data(flow.request.urlencoded_form))
        self.page_config['DIR'] = cfda_page_dir
        self.page_config['file_name'] = '{}_第{}页.html'.format(
            self.page_config['tableName'],
            self.page_config['curstart']
        )
        if self.page_config['index'] >= 15:
            self.page_config['index'] = 1
    else:
        update_config({'is_request_end': '1'})
        return

    text = flow.response.get_text()
    # 创建路径 路径设置的规约 详情和翻页要分开
    dir_exists(self.page_config['DIR'])
    file_path = "{}/{}".format(self.page_config['DIR'], self.page_config['file_name'])
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(text)

    _config1 = {
        'curstart': self.page_config['curstart'],
        'index': self.page_config['index'],
        'is_request_end': '1',
        'response_status_code': flow.response.status_code,
        'index2': self.page_config['index2']
    }
    print(_config1)
    update_config(_config1)


def clientdisconnect(self, layer: mitmproxy.proxy.protocol.Layer):
    """
        A client has disconnected from mitmproxy.
    """


addons = [
    Counter()
]
