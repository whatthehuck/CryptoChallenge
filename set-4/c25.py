#!/usr/bin/env python
#coding=utf8
import random
from Crypto.Cipher import AES
import struct
import base64
import string
def ctrencrypt(s,nonce,key,blksize=16):    #ctr加密函数
 return ctrdecrypt(s,nonce,key,blksize)
def ctrdecrypt(c, nonce, key, blksize=16):
        a = AES.new(key, AES.MODE_ECB)  #新建一个AES加密模块 
        m = ""  #输出
        ctr = 0 #ctr计数器 开始置0
        for i in range(0,len(c),16): #把密文流按16大小分开
                stream = a.encrypt(struct.pack("<Q",nonce)+struct.pack("<Q",ctr))
                #用struct 的pack将  noce|ctr  打包成2进制流  例如ctr=1时为  \x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00 
                #然后把这串2进制aes加密
                for (c1, c2) in zip(stream,c[i:i+16]): #用zip将 密文和stream流的内容对应打包 并赋值给c1 c2
                        m += "".join(chr(ord(c1)^ord(c2))) #对应异或
                ctr += 1 #本轮结束 ctr+1
        return m
p=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','w','v','u','x','y','z','1','2','3','4','5','6','7','8','9','0'], 16)).replace(" ","")
q=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','w','v','u','x','y','z','1','2','3','4','5','6','7','8','9','0'], 8)).replace(" ","")#随机生成密钥以及盐
class ctredit:      #
  def __init__(self,data):
    self.key = p
    self.nounce = int(q.encode('hex'),16)
    self.encdata = ctrencrypt(data,self.nounce,self.key)
  def getdata(self):
    return self.encdata
  def edit(self,offset,text):  #判断offset+test对于解密后数据的长度
    if offset < 0:
      return False
    if offset + len(text) > len(self.encdata):
      return False
    if len(text) == 0:
      return False
    data = ctrencrypt(self.encdata,self.nounce,self.key)  #对数据进行加密
    tmp = data[:offset]+text+data[len(text)+offset:]   #转化中间过程
    self.encdata = ctrencrypt(tmp,self.nounce,self.key)#解密
    return True

if __name__ == "__main__":
  fq = open("asd.txt")#对该文档进行恢复明文操作之后利用ctr模式对其进行加密，放在同目录下即可，一同传过去了
  data=fq.read()#读取数据
  obj = ctredit(base64.b64decode(data))#解开base64编码	
  enc0 = obj.getdata()#ecb解密
  if obj.edit(0,"a"*len(enc0)):
    enc1 = obj.getdata()
    key = "".join([ chr(ord(c)^ord("a")) for c in enc1])#生成解密最后明文的key
    txt0 = "".join([ chr(ord(k)^ord(c)) for k,c in zip(key,enc0)])#生成明文
    print txt0.encode('hex')
