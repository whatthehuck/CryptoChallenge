c = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"


def strxor(a, b):
    #逐个byte进行XOR,并添加到返回字符串中
    tmp =  "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a.decode('hex'), b.decode('hex'))])
    if  32 <= ord(tmp) <= 127:
        return tmp
    else:
        return ""
    

for i in range(0x10,0x100):
    tmp = hex(i).replace('0x','')
    test = ""
    for each in range(0,len(c),2):
        each_hex =  c[each:each+2]
        test = test + strxor(tmp,each_hex)
    nice = 0
    for each in test:
        if 32 <= ord(each) <= 126:
            nice += 1
    if nice == len(c)/2:
        print hex(i),test
    #暴力破解，将所有能解出来的值列出来，然后肉眼查找
