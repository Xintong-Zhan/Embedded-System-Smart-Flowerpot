#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306

import requests
import json

import socket  # 导入 socket 模块
import time

def get_host_ip():
	try:
	     s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	     s.connect(('8.8.8.8', 80))
	     ip = s.getsockname()[0]
	finally:
	     s.close()
	return ip


ip=get_host_ip() #Ip addr
print(ip)
s = socket.socket()  # 创建 socket 对象

port = 80  # 设置端口
s.bind((ip, port))  # 绑定端口

s.listen(1)  # 等待客户端连接

#s.settimeout(1)
#serial = i2c(port=1, address=0x3C)
#device = ssd1306(serial,width=128,height=32)


while True: 
    c,addr= s.accept()  # 建立客户端连接     
    tx_data="raspberry pi connected!"
    c.send(str.encode(tx_data))
    tx_response="HTTP/1.1 200 OK\r\n\r\n welcome!"
    c.send(str.encode(tx_response))
    rx_data=c.recv(1048).decode('utf-8')
    print(rx_data)
    time.sleep(1)

