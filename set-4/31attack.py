#! --coding:utf-8-- !#
import os
import datetime


#时间攻击主程序
s='"http://localhost:9000/test?file=foo&signature='
mac='0'*40


List=[]
for i in range(48,58):
	List.append(chr(i))
for i in range(97,123):
	List.append(chr(i))
#将小写字母和数字添加到列表中，方便后面提取
#print len(List)
#s1=''
#s1=s+mac
#number=500000
#print s1
s2 = 'python 31.py '+s
s3=""
#print List[1]
for num in range(len(mac)):
	# s1=s+mac
	#os.system("python 31.py "+s1)
	i=0 #初始化 
#	print num
	for i in range(len(List)):
		mac=mac[:num]+List[i]+mac[num+1:]  #构造MAC的过程
#		print mac[:num]
#		print i
#		print num
#		print List[i]
#		print mac[num+1:]
#		print mac
		# print num
		s3 = s2+mac+'"' #构造命令行参数
#		print s3
		d1 = datetime.datetime.now()  #获取当前时间
		os.system(s3)    #调用命令行
		d2 = datetime.datetime.now()  #获取当前时间，之后通过时间差来判断
#		print d1
#		print d2
#		print (d2-d1).microseconds
#		print ((num+1)%2)*500000
#		print (d2-d1).seconds
#		print (num+1)/2
		if ((d2-d1).microseconds > ((num+1)%2*500000)) & ((d2-d1).seconds >= (num+1)/2):  #通过返回时间来判断该字节是否正确
#			mac[num] == i
			print "-----------------"
			print mac
			print "-----------------"
			break

#for i in range(40):
#	for j in range(97):

print mac
