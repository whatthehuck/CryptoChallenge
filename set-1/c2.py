def strxor(a, b):
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a.decode('hex'), b.decode('hex'))])
    #逐个byte进行XOR,并添加到返回字符串中
t_1 = "1c0111001f010100061a024b53535009181c"
t_2 = "686974207468652062756c6c277320657965"
t_3 = "746865206b696420646f6e277420706c6179"


if __name__ == "__main__":
    print strxor(t_1,t_2).encode('hex')
