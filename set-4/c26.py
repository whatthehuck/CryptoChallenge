#!/usr/bin/env python
#coding:utf-8
import string
import random
from Crypto.Cipher import AES
import struct

p=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','w','v','u','x','y','z','1','2','3','4','5','6','7','8','9','0'], 16)).replace(" ","")
q=string.join(random.sample(['a','b','c','d','e','f','g','h','i','j','k','l','n','m','o','p','q','r','s','t','w','v','u','x','y','z','1','2','3','4','5','6','7','8','9','0'], 8)).replace(" ","")
#creat random nonce and key

def decrypt(c, nonce, key):#定义解密函数
        a = AES.new(key, AES.MODE_ECB)  #新建一个AES加密块 
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
		
class rep:
  def __init__(self):#定义变量
    self.n = int(q.encode('hex'),16)
    self.k = p
  def myinput(self,s): 
    s = s.replace(";","\;").replace("=","\=")
    pre = "comment1=cooking%20MCs;userdata="
    lat = ";comment2=%20like%20a%20pound%20of%20bacon"
    return decrypt(pre+s+lat,self.n,self.k)
  def output(self,s):#print padding
	  return decrypt(s,self.n,self.k)

if __name__ == "__main__":
  txt = "abc;admin=true"#padding	
  t = rep()
  enc = t.myinput("a"*len(txt))  
  key = [ ord(c)^ord("a") for c in enc[32:32+len(txt)] ]#产生cbc解密key 把32位后的c和“a”异或抵消解密"A"
  test = enc[:32]+"".join([chr(ord(c)^k) for c,k in zip(txt,key)])+enc[32+len(txt):] #产生cbc密文
  print t.output(test)  #打印明文
  


