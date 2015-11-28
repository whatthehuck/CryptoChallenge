base64_m = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
hex_m = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"

m = "I'm killing your brain like a poisonous mushroom"
def pad(base64_code):
    #对base64进行补齐
    tmp = len(base64_code) % 4
    if tmp != 0:
        return base64_code + "="*tmp

def bin_base64_box(bin_num):
    #bin_to_base64 的转换盒
    if 0 <= bin_num <= 25:
        return chr(0x41 + bin_num)
    if 26 <= bin_num <= 51:
        return chr(0x61 + bin_num - 26 )
    if 52 <= bin_num <= 61:
        return chr(0x30 + bin_num - 52 )
    if bin_num == 62:
        return "+"
    if bin_num == 63:
        return "/"
    else:
        print "bin_base_box_Error: Over_index"

def bin_base64(bin_num):
    #将bit转为一个base64字符
    first = ord(bin_num[0])
    second = ord(bin_num[1])
    thrid = ord(bin_num[2])
    
    o_1 = first // 4
    o_2 = ( first % 4 ) * 2 ** 4 + second // ( 2 ** 4 ) 
    o_3 = second % ( 2 ** 4 ) * 2 ** 2 + thrid // ( 2 ** 6 )
    o_4 = thrid % ( 2 ** 6 )
    
    output = bin_base64_box(o_1) + bin_base64_box(o_2) + bin_base64_box(o_3) + bin_base64_box(o_4)
    return output
    

def hex_To_base64(hex_code):
    #hex转换为base64
    hex_box = []
    for i in range(0,len(hex_code),6):
        hex_box.append(hex_code[i:i+6])
    base64_output = ""
    for i in hex_box:
        bin_tmp = i.decode('hex')
        base64_output = base64_output + bin_base64(bin_tmp)
    return base64_output

#####################################################################################
def base64_bin_box(bin_num):
    #base64_to_bin 的转换盒
    tmp = ord(bin_num)
    if ord('A') <= tmp <= ord('Z'):
        return tmp - ord('A')
    if ord('a') <= tmp <= ord('z') :
        return tmp - ord('a') + 26
    if ord('0') <= tmp <= ord('9'):
        return tmp - ord('0') + 52
    if bin_num == '+':
        return 62
    if bin_num == '/':
        return 63
    if bin_num == '=':
        return 0
    else:
        print "base64_bin_box_Error: Over_index"
    
def base64_bin(base64_chr):
    #获取一位base64转为bit
    first = base64_bin_box(base64_chr[0])
    second = base64_bin_box(base64_chr[1])
    thrid = base64_bin_box(base64_chr[2])
    fourth = base64_bin_box(base64_chr[3])
    
    o_1 = first * 4 + second // ( 2 ** 4 )
    if len(hex(o_1).replace('0x','')) == 1:
        o_1 = "0"+hex(o_1).replace('0x','')
    else:
        o_1 = hex(o_1).replace('0x','')
        
    o_2 = ( second % ( 2 ** 4 ) ) * 2 ** 4 + thrid // ( 2 ** 2 )
    if len(hex(o_2).replace('0x','')) == 1:
        o_2 = "0"+hex(o_2).replace('0x','')
    else:
        o_2 = hex(o_2).replace('0x','')
        
    o_3 = ( thrid % ( 2 ** 2 ) ) * 2 ** 6 + fourth
    if len(hex(o_3).replace('0x','')) == 1:
        o_3 = "0"+hex(o_3).replace('0x','')
    else:
        o_3 = hex(o_3).replace('0x','')
        
    output =  o_1 + o_2 + o_3
    return output    

def base64_To_hex(base64_code):
    #base64转为hex
    base64_box = []
    for i in range(0,len(base64_code),4):
        base64_box.append(base64_code[i:i+4])
    base64_output = ""
    for i in base64_box:
        if len(i) % 4 != 0:
            i = pad(i)
        base64_output = base64_output + base64_bin(i)
    return base64_output
    
if __name__ == "__main__":
    print hex_To_base64(hex_m)
    print base64_m

    print hex_m

