#!--coding:utf-8--!#

def profile_for(E_mail):
    profile = {}
    profile['email'] = E_mail
    profile['uid'] = 10
    if "=" in E_mail or "&" in E_mail:
        print "profile ERROR: Illegal input '&' or '='"
        return None
    if E_mail == "shinukami@fedoral.com":
        profile['role'] = 'admin'
    else:
        profile['role'] = 'user'
    return profile

def Encode_Dict(Dict):
    re = "".join(i+"="+str(Dict[i])+"&" for i in Dict)
    re = re[:-1]
    return re
        
def Decode_to_Dict(Str):
    re = {}
    data = Str.split("&")
    for i in data:
        part = i.split("=")
        re[part[0]]=part[1]
    return re


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
    return encobj.encrypt(plaintext).encode('hex')

def decrypt_block(key, ctxt):
    decobj = AES.new(key, AES.MODE_ECB)
    return decobj.decrypt(ctxt).encode('hex')

def encrypt_ecb(key,plaintext):
    if(len(plaintext) % len(key) != 0):
        plaintext = pad(plaintext,len(key))
    blocks = [plaintext[x:x+len(key)] for x in range(0,len(plaintext),len(key))]
    ctxt = ""
    for i in range(0,len(blocks)):
        ctxt = ctxt + encrypt_block(key,blocks[i])
    return ctxt

def decrypt_ecb(key,ctxt):
    ctxt = ctxt.decode('hex')
    blocks = [ctxt[x:x+len(key)] for x in range(0,len(ctxt),len(key))]
    PT = ""
    for i in range(0,len(blocks)):
        PT = PT + decrypt_block(key,blocks[i]).decode('hex')
    return PT

key = "18543c894852b3a1ecaa34de4fbfaa37".decode('hex')

def profile(data):
    a =  profile_for(data)
    b = Encode_Dict(a)
    c = encrypt_ecb(key,b)
    return c

def parse(data):
    a = decrypt_ecb(key,data)
    item = []
    a = a.split("&")
    if "role=admin" in a:
        print "You are Admin !\n"
    else:
        print "You aren't Admin\n"
    return a



if __name__ == '__main__':



    print'''
#########################################################
## ##                                               # # #
# # #    #######    EEEEEEE     SSSSS    #######    ## ##
## ##       #      EE          S     S      #       # # #
# # #      #      EEEEEEE       SSS        #        ## ##
## ##     #      E           S     S      #         # # #
# # #    #      EEEEEEE       SSSSS      #          ## ##
## ##                                               # # #
#########################################################

'''

    print profile("HAO@168.com")
    print parse("5bee70a44ae1a63967c511d4fab7a1ec5f0675dd8f74ca90ef2274a5d0c183d141402dab2cb96b706856f62daf4b7b33")



    print profile("shinukami@fedoral.com")
    print parse("8e9d636f367af1657b05ae80a4a47c53bab9d5b10c4c4eea480615e497a935005bf92c7fe1e6967324909f5cad039808")
