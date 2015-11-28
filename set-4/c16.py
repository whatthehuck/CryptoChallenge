#!--coding:utf-8--!#

from Crypto.Cipher import AES

#pad
def pkcs7pad(s,blksize=16):
    missing = abs(len(s) - (len(s)/blksize+1) * blksize)
    return s+(chr(missing)*missing)

#padcheck
def pkcs7chk(s,blksize=16):
    padlen = ord(s[-1])
    assert padlen <= blksize, 'pad length wrong'

    sl = len(s)-1
    for i in range(padlen):
        assert ord(s[sl - i]) == padlen, "wrong padding"
    return s[:sl-padlen+1]

#CBC-en
def cbcencrypt(s,iv,key,blksize=16):
    assert len(iv) == blksize, 'IV is not equal to blocksize'
    a = AES.new(key,AES.MODE_ECB)
    s = pkcs7pad(s,blksize)
    out = ""

    for i in range(0,len(s),blksize):
        mx = "".join([chr( ord(c1) ^ ord(c2) ) for (c1, c2) in zip(  iv, s[i:i+blksize])])
        iv = a.encrypt(mx)
        out += iv
    return out

#CBC-de
def cbcdecrypt(s,iv,key,blksize=16):
    assert len(iv) == blksize, 'IV is not equal to blocksize'
    a = AES.new(key,AES.MODE_ECB)
    out = ""

    for i in range(0,len(s),blksize):
        enc = a.decrypt(s[i:i+blksize])
        out += "".join([chr(ord(c1)^ord(c2)) for (c1,c2) in zip(iv,enc)])
        iv = s[i:i+blksize]

    return pkcs7chk(out)

#input
def myinput(s,iv,key):
    s = s.replace(";","\;").replace("=","\=")
    prefix = "comment1=cooking%20MCs;userdata="
    suffix = ";comment2=%20like%20a%20pound%20of%20bacon"

    return cbcencrypt(prefix+s+suffix,iv,key)


#check_if you are admin
def checkadmin(s,iv,key):
    if ";admin=true;" in cbcdecrypt(s,iv,key):
        return True
    return False

if __name__ == "__main__":

    iv = open("/dev/urandom").read(16)
    key = open("/dev/urandom").read(16)

    enc = myinput("a"*16+":admin<true",iv,key) #输入
    test1 = chr(ord(enc[32])^1)+enc[33:38]+chr(ord(enc[38])^1)+enc[39:48] #逐字进行XOR
    test = enc[:32]+test1+enc[48:] #格式化密文
    if checkadmin(test,iv,key) == True: # 检查是否为admin
        print "we did good ;)"
    else:
        print "Failed !"





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
