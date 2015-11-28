#!/usr/bin/env python
#! --coding:utf-8-- !# 

import c16
import sys
from random import Random


class c27:
  

  
  def __init__(self):
    self.key =''
    chars = 'AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    length = len(chars) - 1
    random = Random()
    for i in range(16):
        self.key+=chars[random.randint(0, length)]
        #前面这部分是生成一个16位的秘钥
    self.iv = self.key
    #这里按照题目要求把key和iv变成相等的
    self.prefix = "comment1=cooking%20MCs;userdata="
    self.suffix = ";comment2=%20like%20a%20pound%20of%20bacon"
  
  
    
  def myinput(self,s):
    s = s.replace(";","\;").replace("=","\=")#这个地方过滤一下，防止出错
    print 'plaintext is : '+self.prefix+s+self.suffix+'\n'
    print 'key is :'+self.key+'\n'
    return c16.cbcencrypt(self.prefix+s+self.suffix,self.iv,self.key)
    #这个函数是cbc模式加密的函数，然后因为要求至少3个block，所以用前缀和后缀把消息放中间，就达到了至少3个block

  def check(self,s):
    txt = c16.cbcdecrypt(s,self.iv,self.key)#这个是cbc模式的解密函数
    for c in txt:
      if ord(c) > 126 or ord(c) < 32:
        raise Exception(txt)
    return True
    #这个函数是检测每个字节是否在ascii允许的范围内（32-126）

if __name__ == "__main__":

  t = c27()
  enc = list(t.myinput("hahahah"))#加密信息并且用list形式保存
  print 'enc is :'+"".join(enc)+'\n' #这是加密之后的信息
  test = "".join(enc[:16]+["\x00"]*16+enc[:16]+enc[16:])#这个地方把加密之后的信息故意填充把密文信息改变之后作为测试
  print 'change enc is :'+test+'\n' #这个是把密文篡改之后的信息
  dec = ""
  try:
    out = t.check(test)#这个函数是检测每个字节是否在ascii允许的范围内（32-126）
    print "no exception, try one more time"
    sys.exit(1)
  except Exception, e:
    dec = str(e)
    print 'error msg:'+dec+'\n' #这里是报错信息，报错信息会泄露key

  key = [chr(ord(c1)^ord(c2)) for c1,c2 in zip(dec[:16],dec[32:48])] #通过泄露信息还原出key
  print 'recover key :'+"".join(key)+'\n'
  txt = c16.cbcdecrypt("".join(enc),"".join(key),"".join(key)) #解密
  print txt.encode('string_escape')  #还原出消息
