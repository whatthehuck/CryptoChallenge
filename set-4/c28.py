#!/usr/bin/env python
#! --coding:utf-8-- !# 

import sys
import struct


def rol32(word,count):
  return (word << count | word >> (32 - count)) & 0xFFFFFFFF  #把word先左移count位与运算word右移32-count位，然后结果与全1和运算

def padding(msglen):

  chunks = int((msglen+9)/64)
  missing_chunks = 64 - abs((chunks*64)-(msglen+9))
  #用64减去最后一个block中的存在的消息和最末尾的表示位，得到的就是需要填充的\x00的个数
  pad = "\x80"
  for i in xrange(0,missing_chunks):
    pad += "\x00"
  pad += struct.pack('>Q',msglen*8)#把消息的位数加到末尾，是消息长度*8

  return pad

class sha1:


  blocksize = 64

  def __init__(self,imsg=""):

    self.__setinit()
    self.mesg = imsg
    self.lmsg = len(imsg)

  def __setinit(self):

    self.h0 = 0x67452301
    self.h1 = 0xEFCDAB89
    self.h2 = 0x98BADCFE
    self.h3 = 0x10325476
    self.h4 = 0xC3D2E1F0

  def __transform(self,w):

    for j in range(16,80):
      w.append(rol32(w[j-3] ^ w[j-8] ^ w[j-14] ^ w[j-16],1))

    a = self.h0
    b = self.h1
    c = self.h2
    d = self.h3
    e = self.h4

    for j in range(0,80):#在80个循环中每一段循环用不同的方式计算，0-20是一种，20-40一种,40-60一种，60-80一种
      if j < 20:
        f = (b & c) | ((~ b) & d)
        k = 0x5A827999
      elif j < 40:
        f = b ^ c ^ d
        k = 0x6ED9EBA1
      elif j < 60:
        f = (b & c) | (b & d) | (c & d)
        k = 0x8F1BBCDC
      else:
        f = b ^ c ^ d
        k = 0xCA62C1D6

      temp = (rol32(a,5) + f + e + k + w[j]) & 0xFFFFFFFF #rol32的算法最开始有解释
      e = d
      d = c
      c = rol32(b,30)
      b = a
      a = temp #这里就是按照算法的要求对abcde进行变换

    self.h0 = (self.h0 + a) & 0xFFFFFFFF
    self.h1 = (self.h1 + b) & 0xFFFFFFFF
    self.h2 = (self.h2 + c) & 0xFFFFFFFF
    self.h3 = (self.h3 + d) & 0xFFFFFFFF
    self.h4 = (self.h4 + e) & 0xFFFFFFFF  #这里按照sha1的原理，把h1h2h3h4h0进行变换，得到新的h带到下一轮计算中

  def digest(self,imsg=""):

    msg = self.mesg
    lmsg = self.lmsg
    if imsg != "":
      msg = imsg
      lmsg = len(imsg)

    msg += padding(lmsg)  #这里把消息和pading连接起来，组成了完整的消息了

    for i in range(0,len(msg)/64):
      self.__transform(list(struct.unpack('>IIIIIIIIIIIIIIII',msg[i*64:(i+1)*64]))) #这里就是以一个block为单位（64位）把每个block带入__transform中，计算出这个h0h1h2h3h4,计算到最后一个block那么h0h1h2h3h4就是我们的sha1了

    out = struct.pack('>IIIII',self.h0,self.h1,self.h2,self.h3,self.h4)
    self.__setinit()
    return out

  def hexdigest(self,imsg=""):
    return self.digest(imsg).encode('hex') #把消息转换为16进制

  

if __name__ == "__main__":
  try:
    msg = sys.argv[1]
  except:
    msg = " hey girl you look so beautiful"

  print 'msg is :'+msg+'\n'
  key = "fe49e3fe5d7"
  print 'key is :'+key+'\n'
  print 'sha1 is :'+sha1(key+msg).hexdigest() #这一步是sha1加密之后转换为16进制
