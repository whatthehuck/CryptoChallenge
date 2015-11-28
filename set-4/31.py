#!-- coding:utf-8 --!#

from Crypto.Hash import HMAC
from Crypto.Hash import SHA
import datetime
import sys
import time
# secret = b'Swordfish'
# h = HMAC.new(secret)
# h.update(b'Hello')
# print h.hexdigest()



#服务器认证部分
def HMAC_SHA1(filename):  #对文件名对应文件计算HMAC
	h1 = SHA.new()
	f1 = open (filename+".txt","r")
#	f1 = filename
	secret = b'01234567890123456789' #the HMAC-key

	h = HMAC.new(secret,None,h1)

	h.update(f1.read())
	f1.close()
	return h.hexdigest()

def verify(Mac,mac):
	for i in range(len(mac)):
		if (Mac[i]!=mac[i]):
#			print Mac[i]
			return False 
		time.sleep(0.5) #单字节正确就停等待0.5秒
	return True
	# if flag 
	# 	print "200"
	# else:
	# 	print "500"
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

	# print filename
#	print mac

	Mac = HMAC_SHA1(filename)
#	print Mac
	if verify(Mac,mac):  #验证MAC值是否正确
		print "200"  #正确返回200
	else:
		print "500"  #错误返回500



if __name__ == '__main__':
	URL=sys.argv[1]  #命令行输入参数
	# fp=(URL,'r')
	# stri=fp.read()
#	print URL

#	os.system(s3)
#	d1 = datetime.datetime.now()
	Servers(URL)  
#	d2 = datetime.datetime.now()
	# print d1
	# print d2
#	Attack()