#!/usr/bin/python3.3
#coding:utf-8
import hashlib
import hmac
import random


#把ASCII转成字符
def i2s(i):
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

#字符串转ASCII
def s2i(s):
  return int(s.encode('hex'),16)

class SRP_server :
#构造函数
  def __init__(self,N,g,k,I,P):
    self.N = N
    self.g = g
    self.k = k
    self.I = I
    self.P = P 

  def recv1(self,I,A):
    self.A = A 
    self.Ic = I # 用户
    self.b = random.randrange(0,9999)# 产生随机数字 为b
    self.salt = str(random.randrange(0,9999))# 产生salt 
    x = s2i(hashlib.sha256(self.salt+self.P).digest())  # x = SHA256(salt|password)
    self.v = pow(self.g,x,self.N) #v = g**x %N
    self.B = (self.k*self.v)+(pow(self.g,self.b,self.N)) #B=kv + g**b % N

  def send1(self):
    return self.salt,self.B #发送salt和B

  def recv2(self,hks):
    u = s2i(hashlib.sha256(i2s(self.A)+i2s(self.B)).digest())# u = integer  of SHA256(A|B)
    S = pow(self.A * pow(self.v,u,self.N),self.b,self.N) #S = S = (A * v**u) ** b % N
    K = hashlib.sha256(i2s(S)).digest() # K = SHA256(S)

    if hks == hmac.HMAC(K,self.salt,hashlib.sha256).digest() and self.I == self.Ic:
      return "OK" #判断 如果接受到mac是否等于原来存的的用户计算的mac 
    else:
      return "No wrong"

class SRP_client :

  def __init__(self,N,g,k,I,P):
    self.N = N
    self.g = g
    self.k = k
    self.I = I
    self.P = P
    self.a = random.randrange(0,9999)
    self.A = pow(self.g,self.a,self.N) # A = g**a%N

  def send1(self):
    return self.I,self.A

  def recv1(self,salt,B):
    self.salt = salt 
    u = s2i(hashlib.sha256(i2s(self.A)+i2s(B)).digest())
    x = s2i(hashlib.sha256(self.salt+self.P).digest()) #x=SHA256(salt|password)
    S = pow(B - self.k * pow(self.g,x,self.N),(self.a+u*x),self.N) #S = (B - k * g**x)**(a + u * x) % N
    self.K = hashlib.sha256(i2s(S)).digest() #K = SHA256(S)

  def send2(self):
    return hmac.HMAC(self.K,self.salt,hashlib.sha256).digest() #hi算mac并发送

if __name__ == "__main__":

  NISTprime = 0xc34f #49999

  s = SRP_server(NISTprime,2,3,'123@321.cn','123') 
  c = SRP_client(NISTprime,2,3,'123@321.cn','123')
  I,A = c.send1() #c发送数据
  s.recv1(I,A) #接受邮箱和  公钥A
  salt,B = s.send1() #发送 salt 和公钥B
  c.recv1(salt,B) #就收salt  公钥B
  print s.recv2(c.send2()) #服务器
