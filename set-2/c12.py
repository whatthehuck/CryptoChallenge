#!--coding:utf-8--!#

import os
from Crypto.Cipher import AES
from random import randint 

#加密前的填充
def pad(PT,block_zise):
    PT_length = len(PT)
    pad_num = block_zise - ( PT_length % block_zise )
    pad_alpha = chr(pad_num)
    PT_pad = PT + pad_alpha * pad_num
    return PT_pad

#按块AES加密
def encrypt_block(key, plaintext):
    encobj = AES.new(key, AES.MODE_ECB)
    return encobj.encrypt(plaintext).encode('hex')

#按块AES解密
def decrypt_block(key, ctxt):
    decobj = AES.new(key, AES.MODE_ECB)
    return decobj.decrypt(ctxt).encode('hex')

#ECB模式加密
def encrypt_ecb(key,plaintext):
    if(len(plaintext) % len(key) != 0):
        plaintext = pad(plaintext,len(key))
    blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
    ctxt = ""
    for i in range(0,len(blocks)):
        ctxt = ctxt + encrypt_block(key,blocks[i])
    return ctxt

#ECB模式解密
def decrypt_ecb(key,ctxt):
    ctxt = ctxt.decode('hex')
    blocks = [ctxt[x:x+len(key)] for x in range(0,len(ctxt),len(key))]
    PT = ""
    for i in range(0,len(blocks)):
        PT = PT + decrypt_block(key,blocks[i]).decode('hex')
    return PT


key = "18543c894852b3a1ecaa34de4fbfaa37".decode('hex')


text = "Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK"

import base64
text = base64.b64decode(text)

def AES_128_ECB(MyText,key):
    PT = MyText + text
    return encrypt_ecb(key,PT)
blocksize = 16

enclen = len(AES_128_ECB("A",key))

output = ""

nextblock = "A"*blocksize
for x in range(0,enclen,blocksize*2):
    attack = nextblock
    nextblock = ""
    for i in range(blocksize):
        attack = attack[1:]
        encryptedblk = AES_128_ECB(attack,key)[x:x+blocksize]
        for c in range(256):
            s = attack + nextblock + chr(c)
            if AES_128_ECB(s,key)[:blocksize] == encryptedblk:
                nextblock += chr(c)
                
                break
    output += nextblock
print "secret msg:\n"+output

