#!/usr/bin/python
#coding:utf-8
from Crypto.Cipher import AES
import base64
import struct


def encrypt(c,nonce,key):
        return decrypt(c,nonce,key)
def decrypt(c, nonce, key):
        a = AES.new(key, AES.MODE_ECB)  #新建一个AES加密模块 
        m = ""  #输出
        ctr = 0 #ctr计数器 开始置0
        for i in range(0,len(c),16): #把密文流按16大小分开
                stream = a.encrypt(struct.pack("<Q",nonce)+struct.pack("<Q",ctr))
                #用struct 的pack将  noce|ctr  打包成2进制流  例如ctr=1时为  \x00\x00\x00\x00\x00\x00\x00\x00\x01\x00\x00\x00\x00\x00\x00\x00 
                #然后把这串2进制aes加密
                for x in range(0,16):#对应进行异或运算
                        if ( (ctr>len(c)/16-1) and x > len(c)%16-1): #处理末尾不够16位的部分
                                break
                        m += "".join( chr(ord(stream[x])^ord(c[i+x])))
                ctr += 1
        return m

txt = base64.b64decode("L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==")

print decrypt(txt,0,"YELLOW SUBMARINE")
#  Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby
x = encrypt("Yo, VIP Let's kick it Ice, Ice, baby Ice, Ice, baby ",0,"YELLOW SUBMARINE")
print base64.b64encode(x)
 #L77na/nrFsKvynd6HzOoG7GHTLXsTVu9qvY/2syLXzhPweyyMTJULu/6/kXX0KSvoOLSFQ==