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
#按块AES 进行 XOR 操作
def xor_block(first,second):
    if(len(first) != len(second)):
        print "Blocks need to be the same length!"
        return -1

    first = list(first)
    second = list(second)
    for i in range(0,len(first)):
        first[i] = chr(ord(first[i]) ^ ord(second[i]))
    return ''.join(first)

#CBC加密模式
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
#CBC模式解密
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
    return ptxt
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



#随即填充
def random_pad(ptxt):
    return os.urandom(randint(5,10)) + ptxt + os.urandom(randint(5,10))

#Oracle主程序
def encryption_oracle(your_input):
    which_to_use = randint(0,1)
    key =  os.urandom(16)
    PT  = random_pad(your_input)
    if which_to_use == 0:
        print "Mode \t=  ECB"
        print "PT \t= ",your_input.encode("hex")
        print "PT_rp \t= ",PT.encode("hex")
        print "key \t= ",key.encode("hex")
        print "*****************************************************************************"
        return encrypt_ecb(key,PT)
    else:
        IV  =  os.urandom(16)
        print "Mode \t=  CBC"
        print "PT \t= ",your_input.encode("hex")
        print "PT_rp \t= ",PT.encode("hex")
        print "IV \t= ",IV.encode("hex")
        print "key \t= ",key.encode("hex")
        print "*****************************************************************************"
        return encrypt_cbc(key,IV,PT)

PT = "Hello,who are you ?"
print "encryption_oracle:\n",encryption_oracle(PT)
