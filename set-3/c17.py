# -*- coding:utf-8 -*-

import random
import base64
import sys
from Crypto.Cipher import AES

#padding check
def paddingcheck(input):
    if len(input)!=16:
        return False
    padding=input[-1]
    #取最后一位为padding长度

    if ord(padding)>16 or ord(padding)==0:
        return False

    for i in range(ord(padding)):
        if input[-(i+1)]!=padding:
            return False
            #对比，padding错误则返回false
    return True

#CBC encrypt and decrypt from set2 10
def pad(PT,block_zise):
    pad_num = block_zise - ( len(PT) % block_zise )
    return PT+ chr(pad_num) * pad_num

def encrypt_block(key, plaintext):
        encobj = AES.new(key, AES.MODE_ECB)
        return encobj.encrypt(plaintext).encode('hex')

def decrypt_block(key, ctxt):
        decobj = AES.new(key, AES.MODE_ECB)
        return decobj.decrypt(ctxt).encode('hex')

def xor_block(first,second):
        if(len(first) != len(second)):
                print "Blocks need to be the same length!"
                return -1

        first = list(first)
        second = list(second)
        for i in range(0,len(first)):
                first[i] = chr(ord(first[i]) ^ ord(second[i]))
        return ''.join(first)

def encrypt_cbc(key,IV, plaintext):
        if(len(plaintext) % len(key) != 0):
                plaintext = pad(plaintext,len(key))
        blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
        for i in range(0,len(blocks)):
                if (i == 0):
                        ctxt = xor_block(blocks[i],IV)
                        ctxt = encrypt_block(key,ctxt)
                else:
                        tmp = xor_block(blocks[i],ctxt[-1 * (len(key) * 2):].decode('hex')) 
                        ctxt = ctxt + encrypt_block(key,tmp)
        return ctxt

def decrypt_cbc(key,IV,ctxt):
        ctxt = ctxt.decode('hex')
        if(len(ctxt) % len(key) != 0):
                print "Invalid Key."
                return -1
        blocks = [ctxt[x:x+len(key)] for x in range(0,len(ctxt),len(key))]
        for i in range(0,len(blocks)):
                if (i == 0):
                        ptxt = decrypt_block(key,blocks[i])
                        ptxt = xor_block(ptxt.decode('hex'),IV)
                else:
                        tmp = decrypt_block(key,blocks[i])
                        tmp = xor_block(tmp.decode('hex'),blocks[i-1])
                        ptxt = ptxt + tmp
        if paddingcheck(ptxt)==False:
            return False
        else:
            return True
            #加上了padding check


#攻击函数
def paddingoracle(key,iv,ct):
    if len(ct)!=32:
        return ""
    test=()
    for guess in range(256):
        newiv=iv[:len(iv)-1]
        newiv+=chr(ord(iv[-1])^1^guess)
        if decrypt_cbc(key,newiv,ct)==True:
            test=test+(guess,)
        #判断多种可能性，用于对付最后一个block
    for each in test:
        result=""
        flag=0
        for padding in range(1,17):
            for guess in range(256):
                newiv=iv[:len(iv)-padding]
                newiv+=chr(ord(iv[len(iv)-padding])^padding^guess)
                for i in range(len(result)):
                    newiv+=chr(ord(result[i])^padding^ord(iv[len(iv)-padding+i+1]))
                #组建新的iv
                if len(newiv)!=16:
                    flag=1
                    break
                    #解密错误，对付最后一个block
                if decrypt_cbc(key,newiv,ct)==False:
                    continue
                else:
                    if padding==1 and guess!=each:
                        continue
                    result=chr(guess)+result
                    break
        if flag==1:
            continue
    return result

msg="MDAwMDAwTm93IHRoYXQgdGhlIHBhcnR5IGlzIGp1bXBpbmc=|\
MDAwMDAxV2l0aCB0aGUgYmFzcyBraWNrZWQgaW4gYW5kIHRoZSBWZWdhJ3MgYXJlIHB1bXBpbic=|\
MDAwMDAyUXVpY2sgdG8gdGhlIHBvaW50LCB0byB0aGUgcG9pbnQsIG5vIGZha2luZw==|\
MDAwMDAzQ29va2luZyBNQydzIGxpa2UgYSBwb3VuZCBvZiBiYWNvbg==|\
MDAwMDA0QnVybmluZyAnZW0sIGlmIHlvdSBhaW4ndCBxdWljayBhbmQgbmltYmxl|\
MDAwMDA1SSBnbyBjcmF6eSB3aGVuIEkgaGVhciBhIGN5bWJhbA==|\
MDAwMDA2QW5kIGEgaGlnaCBoYXQgd2l0aCBhIHNvdXBlZCB1cCB0ZW1wbw==|\
MDAwMDA3SSdtIG9uIGEgcm9sbCwgaXQncyB0aW1lIHRvIGdvIHNvbG8=|\
MDAwMDA4b2xsaW4nIGluIG15IGZpdmUgcG9pbnQgb2g=|\
MDAwMDA5aXRoIG15IHJhZy10b3AgZG93biBzbyBteSBoYWlyIGNhbiBibG93"

if __name__ == "__main__":
    key=random._urandom(16)
    iv=random._urandom(16)

    ct=encrypt_cbc(key,iv,base64.b64decode(random.choice(msg.split('|'))))
    result=paddingoracle(key,iv,ct[0:32])
    #第一个block
    for i in range(32,len(ct),32):
        result+=paddingoracle(key,ct[i-32:i].decode("hex"),ct[i:i+32])
        #接下来的block

    print result
    
    


