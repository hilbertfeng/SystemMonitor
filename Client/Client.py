#!/usr/bin/env python
# -*- coding: UTF-8 -*-

"""
    Created by zhoupan on 7/23/16.
"""

import threading
from socket import *
from time import sleep
import simplejson
# 导入配置类
from Configure import Configure
# 导入配置类
from SystemResource import SystemResource


class Client(threading.Thread):
    """
        客户端，主要将信息发送给服务器
    """

    def __init__(self, thread_id, thread_name):
        threading.Thread.__init__(self)
        threading.thread_id = thread_id
        threading.name = thread_name
        # 端口
        self.port = int(Configure().read_config('client.conf', 'server', 'port'))
        # IP
        self.host = Configure().read_config('client.conf', 'server', 'host')
        # buffer
        # self.buf_size = Configure.read_config('client.conf', 'buffer', 'size')
        # sleep time
        self.sleep_time = int(Configure().read_config('client.conf', 'client', 'sleep'))

    def run(self):
        """线程运行的方法，功能是每隔十秒钟，向服务器发送一下主机信息"""
        sr = SystemResource
        init_data = {
            'cpu': sr.get_cpu_info(self),
            'mem': sr.get_men_info(self),
            'net': sr.get_net_info(self),
            'disk': sr.get_disk_info(self),
            'user': sr.get_user_info(self),
            'port': sr.get_port_info(self)
        }

        while True:
            tcpclinet = socket(AF_INET, SOCK_STREAM)
            tcpclinet.connect((self.host, self.port))
            sr = SystemResource()
            # 将列表数据转转换成字符串
            data = sr.return_all_info(init_data)
            print(data)
            # 保存原旧数据
            init_data = data
            data = simplejson.dumps(data)
            # 将数据发送出去
            tcpclinet.send(data.encode())
            # 关闭连接
            tcpclinet.close()

            # 休眠十秒钟
            sleep(self.sleep_time)


if __name__ == '__main__':
    thread = Client(1, 'first')
    thread.start()
