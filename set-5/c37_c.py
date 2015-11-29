#!/usr/bin/env python
#coding:utf-8

import random 
from c36 import SRP_client,i2s
import hashlib
import hmac
import socket
import os


if __name__ == "__main__":
  NISTprime = 0xc34f #定义大素数 

  print "Normal login:", 
  c = SRP_client(NISTprime,2,3,'a@a.com','abc') #测试正常的mac验证
  client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client.connect(("127.0.0.1", 9001))#链接服务器

  I,A = c.send1()#获取用户名和  公钥A
  client.send(str(I)+","+str(A)) #发送I和A
  data = client.recv(4096)
  salt,B = data.split(",") #接收服务器的数据传回的salt 和服务器公钥B
  c.recv1(salt,int(B)) #生成 u x s k
  client.send(c.send2()) #计算mac并发送
  print client.recv(4096) #显示服务器返回的结果
  client.shutdown(2)

  print "Attack A=0 (because of this S = 0):",

  client1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client1.connect(("127.0.0.1", 9001))
  client1.send("a@a.com,0") #发送A = 0
  data = client1.recv(4096)
  salt = data.split(",")[0]
  K = hashlib.sha256(i2s(0)).digest() #计算K 
  client1.send(hmac.HMAC(K,salt,hashlib.sha256).digest()) #计算mac并发送
  print client1.recv(4096)
  client1.shutdown(2)

  print "Attack A=N (because of this S = 0):",

  client2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client2.connect(("127.0.0.1", 9001))
  client2.send("a@a.com,"+str(NISTprime)) #发送A = N
  data = client2.recv(4096)
  salt = data.split(",")[0]
  K = hashlib.sha256(i2s(0)).digest()
  client2.send(hmac.HMAC(K,salt,hashlib.sha256).digest())
  print client2.recv(4096)
  client2.shutdown(2)

  print "Attack A=N*2 (because of this S = 0):",

  client3 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  client3.connect(("127.0.0.1", 9001))
  client3.send("a@a.com,"+str(NISTprime*2)) #发送A  = N*2
  data = client3.recv(4096)
  salt = data.split(",")[0]
  K = hashlib.sha256(i2s(0)).digest()
  client3.send(hmac.HMAC(K,salt,hashlib.sha256).digest())
  print client3.recv(4096)
  client3.shutdown(2)
