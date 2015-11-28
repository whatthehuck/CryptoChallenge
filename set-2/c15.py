#!--coding:utf-8--!#


#pad_alpha = chr(pad_num)
#pad_num   = 块长度 - 明文 % 宽长度
def padding(PT,block_zise):
    PT_length = len(PT)
    pad_num = block_zise - ( PT_length % block_zise )
    pad_alpha = chr(pad_num)
    PT_pad = PT + pad_alpha * pad_num
    return PT_pad


def check_padding(Padded_PT):
    test = Padded_PT[::-1]
    lsb = test[0]
    lsb_count = ord(lsb)
    for i in range(lsb_count):
        if test[i] != lsb:
            print "Bad Padding !"
            return False
    return True

if __name__ == "__main__":
    a = padding("aads12345",8)
    print check_padding(a)
    print check_padding("6164733132333435080808080808080809".decode('hex'))
