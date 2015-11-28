#!/usr/bin/env python
#! --coding:utf-8-- !# 


from rsa import RSA # RSA算法
import math
import hashlib
from decimal import *

def i2s(i):
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

def s2i(s):
  return int(s.encode('hex'),16)

class PKCS15:


  def pad(self,msg,k):
    fflen = k - 20 - 13  #  k是密钥的长度，fflen表示的是随机字符串的长度，这里用\xff表示随机字符串
    return "\x00\x01%s\x00%s" % ("\xff" * fflen, msg)

  def unpad(self,msg):
    if msg[0:2] == '\x00\x01':
      i = msg.find('\x00', 2)
      return msg[i+1:i+1+20] #从填充完的包里取出来我们的msg
    return None

class RSAsign:

  def make(self,msg,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.sha1(message).digest() #计算msg的sha1
    paddgst = pkcs15.pad(dgst,len(i2s(key[1]))) #把sha1进行填充，填充函数在前面有解释
    return rsa.encrypt(paddgst,key) #调用rsa加密的方法进行加密，c39中有rsa的算法

  def verify(self,msg,sign,key):
    pkcs15 = PKCS15()
    rsa = RSA()
    dgst = hashlib.sha1(message).digest()
    return pkcs15.unpad("\x00"+rsa.decrypt(sign,key)) == dgst #把密文sign和key通过解密函数解密出来，然后在填充之后的包里把msg恢复出来对比一下

def forging(mesg,key):

  e = key[0]
  n = key[1]

  if e != 3:    #检查e是不是3
    raise Exception("e not equal 3")
  pkcs15 = PKCS15()
  dgst = hashlib.sha1(mesg).digest() #计算消息的sha1
  keylen = len(i2s(n)) #密钥长度

  getcontext().prec = keylen * 8 #这里是设置精度


  forge = "\x00\x01%s\x00%s" % ("\xff" * 8, dgst) # 填充过程
  garbage = "\x00" * (keylen - 8 - len(dgst) - 13)
  whole = s2i(forge+garbage)
  cr = int(pow(whole,Decimal(1)/Decimal(3)))+1 #把我们得到的whole开3次方，得到的应该是我们伪造的加密sign

  return i2s(cr) #转换为字符串

if __name__ == "__main__":

  message = "hi mom"
  print 'msg is :'+message+'\n'
  re = RSA()
  pub1,priv1 = re.keygen(l=512,s=False) #通过c39里的函数获得密钥

  rs = RSAsign()
  sign = rs.make(message,priv1) #调用函数算出sign的rsa加密之后的结果
  print 'rsa sign is :'+''.join(sign)+'\n'
  if rs.verify(message,sign,pub1): #这个地方是验证如果成功就输出ok
    print "sign is correct \n"
  else:
    print 'sign is incorrect \n'

  signf = [ forging(message,pub1) ] #这个利用公钥和消息我们可以伪造出一个signf
  print 'signf is :'+''.join(signf)+'\n'
  if rs.verify(message,signf,pub1): #这个地方是验证
    print "sign is correct \n"
  else:
    print 'sign is incorrect \n'
