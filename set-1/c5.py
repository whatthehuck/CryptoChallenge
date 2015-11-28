key = "ICE"
m_1 = """Burning 'em, if you ain't quick and nimble
I go crazy when I hear a cymbal"""

#将2个字符按值进行XOR返回一个hex
def chr_XOR(a,b):
    
    temp = hex(ord(a) ^ ord(b)).replace('0x','')
    if len(temp) == 2:
        return temp
    else:
        temp = "0" + temp
        return temp
    
#利用一个字符串对一个另字符串进行按块XOR
def encrypt_string(key,PT):
    CT = ""
    K_L = len(key)
    M_L = len(PT)
    count = 0
    for PT_chr in PT:
        K_chr = key[count]
        CT = CT + chr_XOR(K_chr,PT_chr)
        count = ( count + 1 ) % 3
    return CT


print encrypt_string(key,m_1)
