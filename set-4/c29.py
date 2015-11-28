#!/usr/bin/env python
# coding:utf8



import c28
import random
import struct


class sha1ext(c28.sha1):
    # orghash  hashed value
    # masglen  信息的长度
    # imsg     添加的信息
    # return   加入padding的填充字符串
    def extlen(self, orghash, msglen, imsg):
        # 按照给定的格式(>IIIII)解析字节流string，返回解析出来的tuple
        hs = struct.unpack(">IIIII", orghash.decode('hex'))

        print "初始信息信息分组:" + str(hs)

        #更改加密算法的初始值
        self.h0 = hs[0]
        self.h1 = hs[1]
        self.h2 = hs[2]
        self.h3 = hs[3]
        self.h4 = hs[4]

        self.mesg = imsg
        tempmsg = c28.padding(msglen) + imsg  # 计算出一个填充值使得 key + message + padding == 512 bits 的整数倍
        self.lmsg = msglen + len(tempmsg)
        return tempmsg


def random_line(afile):
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line.strip() + "::"


if __name__ == "__main__":
   

    try:
        key = random_line(open("words.txt"))  # 词库中随机随机取出一个单词
    except:
        print "can't open words will use secret word \"secret\""
        key = "secret"  # 打开文件失败默认给key赋值

    msg = "comment1=cooking%20MCs;userdata=foo;comment2=%20like%20a%20pound%20of%20bacon"  # 构建扩展攻击的信息
    orghash = c28.sha1(key + msg).hexdigest()  # 对消息进行加密
    print "初始值: key+msg"
    print orghash + " => " + key + msg

    msg2add = ";admin=true"
    att = sha1ext()
    add = att.extlen(orghash, len(key + msg), msg2add)
    print "不知道key得到hash "
    print att.hexdigest()
    print "与使用key进行加密的对比"
    print c28.sha1(key + msg + add).hexdigest() + " => " + key + msg + add.encode('string_escape')
