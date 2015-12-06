def lfet(cc): # letter frequency for english tes
    lfe = { "e": 12,"t": 9,"a": 8,"o": 7,"h": 6,"i": 6,"n": 6,"s": 6,"r": 5,"d": 4,"l": 4,"c": 2,"f": 2,"g": 2,"m": 2,"u": 2,"w": 2,"b": 1,"p": 1,"y": 1 }
    count = 0
    for c in lfe:
        if cc.get(c,0) >= lfe[c]/float(100):
            count += 1
        if count > 2:
            return True
    return False

def cfs(k,s): # character frequency from string
    chars = dict()

    for cc in s:
        c = chr(k^ord(cc)).lower()

        if not c in '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~ \t\n\r\x0b\x0c':
            return None

        chars[c] = chars.get(c,0) + 1
    return chars


def fcxor(ct): # find one character xor
    for key in range(256): # 检查所有可能的值
        chars = cfs(key,ct)
        if chars == None:
            continue
        for c in chars:
            chars[c] = chars[c]/float(len(ct))
        if chars.get(' ',0) > 0.1 and lfet(chars):
            return (key, "".join([chr(key^ord(c)) for c in ct]))


def findkeylen(ct,keylen,blocks=5): # 计算块汉明距离相同的密钥长度
    return sum(hd(ct[i:i+keylen],ct[i+keylen:i+keylen*2])/float(keylen) for i in range(0,keylen*blocks,keylen))/blocks

def ch2bin(s): # 字符转换为bit
    return "".join([ bin(ord(c)).replace("0b","").zfill(8) for c in s ])

def hd(s1, s2): # 计算汉明距离
    return sum(c1 != c2 for c1, c2 in zip(ch2bin(s1), ch2bin(s2)))

def reorderblk(ct,keylen):
    blks = [ list() for i in range(keylen) ]
    for i in range(0,len(ct),keylen):
        if i+keylen < len(ct):
            txt = ct[i:i+keylen]
            for j in range(keylen):
                blks[j].append(txt[j])
    return blks


import base64


data = open("6.txt").read()

ct = base64.b64decode(data)
key_len = dict()
for kl in range(2,40):
    key_len[kl] = findkeylen(ct,kl)

for kl in sorted(key_len , key = key_len.get):
    sxor = reorderblk(ct,kl)
    key = ""
    for i in range(kl):
        txt = fcxor("".join(sxor[i]))
        if txt != None:
            key += chr(txt[0])
        else:
            key += chr(0)

    if not '\x00' in key:
        print str((kl,key))
        break


