#!--coding:utf-8--!#

#pad_alpha = chr(pad_num)
#pad_num   = 块长度 - 明文 % 宽长度
def padding(PT,block_zise):
    PT_length = len(PT)
    pad_num = block_zise - ( PT_length % block_zise )
    pad_alpha = chr(pad_num)
    PT_pad = PT + pad_alpha * pad_num
    return PT_pad

if __name__ == "__main__": 
    print len(padding("ads12345",8))
