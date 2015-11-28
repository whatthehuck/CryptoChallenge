#!-- coding:utf-8 --!#

from Crypto.Hash import HMAC
from Crypto.Hash import SHA
import datetime
import sys
import time
import socket


#服务器认证部分
def HMAC_SHA1(filename):  #对文件名对应文件计算HMAC
	h1 = SHA.new()
	f1 = open (filename+".txt","r")
	secret = b'01234567890123456789' #the HMAC-key

	h = HMAC.new(secret,None,h1)

	h.update(f1.read())
	f1.close()
	return h.hexdigest()

def verify(Mac,mac):
	for i in range(len(Mac)):
		if (Mac[i]!=mac[i]):
			return False 
		time.sleep(0.05) #单字节正确就停等待0.05秒
	return True

def Servers(s):
	head=0  #URL的文件名头位置
	end=0  #URL的文件名尾位置
	filename = ""  
	mac = ""
	for i in range(len(s)-4):
		if ((s[i]=='f') & (s[i+1]=='i') & (s[i+2] == 'l') & (s[i+3] == 'e')):   #匹配file字串
			for j in range (i,len(s)-1):
				if (s[j] == '='): #获取=位置
					head = j+1  
				if (s[j] == '&'): #获取&位置
				    end = j
				    break
		 	break
	filename=s[head:end]
	mac = s[end+11:]


	Mac = HMAC_SHA1(filename)
	if verify(Mac,mac):  #验证MAC值是否正确
		print "200"
		return "200"  #正确返回200
	else:
		print "500"
		return "500"  #错误返回500



if __name__ == '__main__':
#	URL=sys.argv[1]  #命令行输入参数
	sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	sock.bind(('',12345))
	sock.listen(5)
	try:
		while(True):
			newSocket,address = sock.accept()
			while True:
				receive=newSocket.recv(81920)
				if not receive:break
			# print receive
				newSocket.sendall(Servers(receive))
			newSocket.close()
	finally:
		sock.close()		
