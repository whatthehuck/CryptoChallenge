#!--coding:utf-8--!#

import sys
from Crypto.Cipher import AES
from random import randint 

def pad(PT,block_zise):
    PT_length = len(PT)
    pad_num = block_zise - ( PT_length % block_zise )
    pad_alpha = chr(pad_num)
    PT_pad = PT + pad_alpha * pad_num
    return PT_pad

def encrypt_block(key, plaintext):
    encobj = AES.new(key, AES.MODE_ECB)
    return encobj.encrypt(plaintext)

def encrypt_ecb(key,plaintext):
    if(len(plaintext) % len(key) != 0):
        plaintext = pad(plaintext,len(key))
    blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
    ctxt = ""
    for i in range(0,len(blocks)):
        ctxt = ctxt + encrypt_block(key,blocks[i])
    return ctxt


text = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"
import base64
import sys
text = base64.b64decode(text)

def encryption_oracle(s,key="",prefix=""):
    s = prefix + s + text
    return encrypt_ecb(key,s)

def findecb(cte,blksize=16):#匹配 ECB 加密模式
    ct = cte.decode('hex')
    a = dict()
    for i in range(0,len(ct),blksize):
        c = ct[i:i+blksize]
        a[c] = a.get(c,0) + 1
        if a[c] > 1:
            return cte

#得到一个随机key
key = open("/dev/urandom").read(16)

#得到一个随机prefix
prefix = open("/dev/urandom").read(randint(1,256))

offset_b = 0
#得到prefix中相同块（如果有的话）之后的不同块
ct1 = encryption_oracle("a", key, prefix)
ct2 = encryption_oracle("b", key, prefix)

for i in range(len(ct1)):
    if ct1[i] != ct2[i]:
        offset = i
        break
print "offset for block with our data: "+str(offset)

#确定块大小
blksize = 1
while True:
    s = ("A"*(blksize*2))*3
    c = encryption_oracle(s, key, prefix)
    if c[offset+blksize:offset+blksize*2] == c[offset+blksize*2:offset+blksize*3]:
        break
    blksize += 1
print "block size: "+str(blksize)

#确定ECB加密模式
if findecb(c.encode('hex'),blksize) == None:
    sys.exit(0)
print "this is ECB mode"

#得到从可控制区开始计算的密文长度
enclen = len(encryption_oracle("a", key, prefix)) - offset
offstr = 0
for i in range(1,blksize*4):
    s = 'A'*i
    if encryption_oracle(s, key, prefix)[offset+blksize:offset+blksize*2] == encryption_oracle(s, key, prefix)[offset+(blksize*2):offset+blksize*3]:
        offstr = i-(blksize*2)
        break
print "ourdata offset inside the block: "+str(offstr)

#
out = ""
nxtblk = "A"*blksize
for x in range(0,enclen,blksize):
    attack = "A"*offstr+nxtblk
    nxtblk = ""
    for i in range(blksize):
        attack = attack[1:]
        encblk = encryption_oracle(attack, key, prefix)[offset+x+blksize:offset+x+blksize*2]
        for c in range(256):
            s = attack + nxtblk + chr(c)
            if encryption_oracle(s, key, prefix)[offset+blksize:offset+blksize*2] == encblk:
                nxtblk += chr(c)
                break
    out += nxtblk   
print "secret msg:\n"+"***********************************************************************"
print out
