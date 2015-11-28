#! --coding:utf-8-- !#
import os
import datetime
import time

import socket






#时间攻击主程序
s='http://localhost:9000/test?file=foo&signature='
mac='0'*40


List=[]
for i in range(48,58):
	List.append(chr(i))
for i in range(97,103):
	List.append(chr(i))
print List
#将小写字母和数字添加到列表中，方便后面提取

#s2 = 'python 32.py '+s
s2=s
s3=""
#print List[1]
n=0
for num in range(len(mac)):

	i=0 #初始化 
	n+=1
	for i in range(len(List)):
		
		mac=mac[:num]+List[i]+mac[num+1:]  #构造MAC的过程
		# print mac[:num]
		# print i
		# print num
		# print List[i]
		# print mac[num+1:]
		# print mac
		# print num
		s3 = s2+mac #构造命令行参数
		sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
		sock.connect(("localhost",12345))
		sock.sendall(s3)
		d1 = datetime.datetime.now()  #获取当前时间
		# os.system(s3)    #调用命令行
		# while True:
		response = sock.recv(81920)
		# print response
		d2 = datetime.datetime.now()  #获取当前时间，之后通过时间差来判断
		sock.close()
		# print d1
		# print d2

		tm1=(d2-d1).microseconds
		tm2=(d2-d1).seconds
		# print str(tm2)+'.'+str(tm1)
		print tm1
		print tm2
#		time.sleep(1)
		if ((tm1>=((n%20)*50000)) & ((tm2>=n/20))):
			# if ((n+1)/20)>(n/20):
			# 	print "-----------------"
			# 	print mac
			# 	print "-----------------"
			# 	break
			# if ((tm1<=((n+1)%20)*50000) & (tm2<=(n+1)/20)):
			# 	print "-----------------"
			# 	print mac
			# 	print "-----------------"
			# 	break
			print "-----------------"
			print mac
			print "-----------------"
			break
		elif (tm1<((n-1)%20)*50000) & (tm2<(n-1)/20) & (n!=0):
			break
		elif (tm2>n/20)&(tm1<((n%20)*50000)):
			print "-----------------"
			print mac
			print "-----------------"
			break
		# if ((tm1>=((n%20)*50000)) & ((tm2>=n/20))):
		# 	if ((n+1)/20)<(n/20):
		# 		print "-----------------"
		# 		print mac
		# 		print "-----------------"
		# 		break
		# 	elif ((tm1<=((n+1)%20)*50000) & (tm2<=(n+1)/20)):
		# 		print "-----------------"
		# 		print mac
		# 		print "-----------------"
		# 		break
		# elif (tm1<=((n-1)%20)*50000+1000) & (tm2<=(n-1)/20):
		# 	break
		# if (tm1 > (n%2*50000)) & (tm2 >= n/2):  #通过返回时间来判断该字节是否正确 
		# 	#mac[num] == i
		# 	print "-----------------"
		# 	print mac
		# 	print "-----------------"
		# 	break

print mac
