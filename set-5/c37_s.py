#!/usr/bin/env python
#coding:utf-8


from c36 import SRP_server
from select import select
import socket
import os
import sys



if __name__ == "__main__":
  NISTprime = 0xc34f#素数

  s = SRP_server(NISTprime,2,3,'a@a.com','abc')#新建服务端

  server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  server.bind(("127.0.0.1", 9001))
  server.setblocking(False)
  server.listen(1)

  while 1:
    accept,[],[] = select([server],[],[],60) #利用select接收数据

    if server in accept:
      conn,addr = server.accept() #获取链接套接字和链接地址

      if os.fork() == 0:
        data = conn.recv(4096) 
        I,A = data.split(",")#得到邮箱和  客户端发来的公钥A
        s.recv1(I,int(A)) #调用recv1产生b  和 salt  最终生成服务器公钥B
        salt,B = s.send1()#发送B
        conn.send(str(salt)+","+str(B))#发送B
        data = conn.recv(4096)#再接收数据
        status = s.recv2(data) #调用recv2获取是否成功
        conn.send(status)#发送是否成功
        sys.exit() # killing the child

    # 清理子程序
    try:
      os.waitpid(0,os.WNOHANG)
    except OSError:
        pass