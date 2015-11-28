#coding:utf8
#!/usr/bin/env python

import sys
import struct
import random

def rol32(word,count):
    return (word << count | word >> (32 - count)) & 0xFFFFFFFF

def r1(a, b, c, d, x, s):
  f = ((b & c) | ((~b) & d))
  return rol32(( a + f + x )             & 0xFFFFFFFF,s)
def r2(a, b, c, d, x, s):
  f = ((b & c) | (b & d) | (c & d))
  return rol32(( a + f + x + 0x5A827999) & 0xFFFFFFFF,s)
def r3(a, b, c, d, x, s):
  f = b ^ c ^ d
  return rol32(( a + f + x + 0x6ED9EBA1) & 0xFFFFFFFF,s)

def padding(msglen):

  chunks = int((msglen+9)/64)
  missing_chunks = 64 - abs((chunks*64)-(msglen+9))

  pad = "\x80"
  for i in xrange(0,missing_chunks):
    pad += "\x00"
  pad += struct.pack('<Q',msglen*8)

  return pad

class md4:
  '''
  https://tools.ietf.org/html/rfc1320

  '''

  blocksize = 64

  def __init__(self,imsg=""):

    self.__setinit()
    self.mesg = imsg
    self.lmsg = len(imsg)

  def __setinit(self):

    self.A = 0x67452301
    self.B = 0xEFCDAB89
    self.C = 0x98BADCFE
    self.D = 0x10325476

  def __transform(self,x):

    a = self.A
    b = self.B
    c = self.C
    d = self.D

    a = r1(a, b, c, d, x[ 0], 3)
    d = r1(d, a, b, c, x[ 1], 7)
    c = r1(c, d, a, b, x[ 2], 11)
    b = r1(b, c, d, a, x[ 3], 19)
    a = r1(a, b, c, d, x[ 4], 3)
    d = r1(d, a, b, c, x[ 5], 7)
    c = r1(c, d, a, b, x[ 6], 11)
    b = r1(b, c, d, a, x[ 7], 19)
    a = r1(a, b, c, d, x[ 8], 3)
    d = r1(d, a, b, c, x[ 9], 7)
    c = r1(c, d, a, b, x[10], 11)
    b = r1(b, c, d, a, x[11], 19)
    a = r1(a, b, c, d, x[12], 3)
    d = r1(d, a, b, c, x[13], 7)
    c = r1(c, d, a, b, x[14], 11)
    b = r1(b, c, d, a, x[15], 19)

    a = r2(a, b, c, d, x[ 0], 3)
    d = r2(d, a, b, c, x[ 4], 5)
    c = r2(c, d, a, b, x[ 8], 9)
    b = r2(b, c, d, a, x[12], 13)
    a = r2(a, b, c, d, x[ 1], 3)
    d = r2(d, a, b, c, x[ 5], 5)
    c = r2(c, d, a, b, x[ 9], 9)
    b = r2(b, c, d, a, x[13], 13)
    a = r2(a, b, c, d, x[ 2], 3)
    d = r2(d, a, b, c, x[ 6], 5)
    c = r2(c, d, a, b, x[10], 9)
    b = r2(b, c, d, a, x[14], 13)
    a = r2(a, b, c, d, x[ 3], 3)
    d = r2(d, a, b, c, x[ 7], 5)
    c = r2(c, d, a, b, x[11], 9)
    b = r2(b, c, d, a, x[15], 13)

    a = r3(a, b, c, d, x[ 0], 3)
    d = r3(d, a, b, c, x[ 8], 9)
    c = r3(c, d, a, b, x[ 4], 11)
    b = r3(b, c, d, a, x[12], 15)
    a = r3(a, b, c, d, x[ 2], 3)
    d = r3(d, a, b, c, x[10], 9)
    c = r3(c, d, a, b, x[ 6], 11)
    b = r3(b, c, d, a, x[14], 15)
    a = r3(a, b, c, d, x[ 1], 3)
    d = r3(d, a, b, c, x[ 9], 9)
    c = r3(c, d, a, b, x[ 5], 11)
    b = r3(b, c, d, a, x[13], 15)
    a = r3(a, b, c, d, x[ 3], 3)
    d = r3(d, a, b, c, x[11], 9)
    c = r3(c, d, a, b, x[ 7], 11)
    b = r3(b, c, d, a, x[15], 15)

    self.A = (self.A + a) & 0xFFFFFFFF
    self.B = (self.B + b) & 0xFFFFFFFF
    self.C = (self.C + c) & 0xFFFFFFFF
    self.D = (self.D + d) & 0xFFFFFFFF

  def digest(self,imsg=""):

    msg = self.mesg
    lmsg = self.lmsg
    if imsg != "":
      msg = imsg
      lmsg = len(imsg)

    msg += padding(lmsg)

    for i in range(0,len(msg)/64):
      self.__transform(list(struct.unpack('<IIIIIIIIIIIIIIII',msg[i*64:(i+1)*64])))

    out = struct.pack('<IIII',self.A,self.B,self.C,self.D)
    self.__setinit()
    return out

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex')



class md4ext(md4):

  def extlen(self,orghash,msglen,imsg):

    hs = struct.unpack("<IIII",orghash.decode('hex'))   #将hashed value分成4组

    #更改了md4加密初始值
    self.A = hs[0]
    self.B = hs[1]
    self.C = hs[2]
    self.D = hs[3]

    self.mesg = imsg
    tempmsg = padding(msglen)+imsg  #添加padding，添加信息放在下一个组
    self.lmsg = msglen + len(tempmsg)  #获取信息的长度
    return tempmsg

def random_line(afile):
  line = next(afile)
  for num, aline in enumerate(afile):
    if random.randrange(num + 2): continue
    line = aline
  return line.strip()+"::"

if __name__ == "__main__":


  try:
    key = random_line(open("words.txt"))
  except:
    print "can't open words.txt will use secret word \"secret\""
    key = "secret"

  msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"
  orghash = md4(key+msg).hexdigest() #对开始信息md4加密
  print "原来的hashed value " + orghash
  msg2add = ";admin=true"  #要添加的字符串
  att = md4ext()
  add = att.extlen(orghash,len(key+msg),msg2add)
  
  print "在不知道key得到的hash "
  print att.hexdigest()  #16进制表示
  print "与使用key进行比较"
  print md4(key+msg+add).hexdigest()+" => "+key+msg+add.encode('string_escape')    
