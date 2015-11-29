# -*- coding: gbk -*-
import sha
import gmpy2

p=gmpy2.mpz(int("800000000000000089e1855218a0e7dac38136ffafa72eda7\
859f2171e25e65eac698c1702578b07dc2a1076da241c76c6\
2d374d8389ea5aeffd3226a0530cc565f3bf6b50929139ebe\
ac04f48c3c84afb796d61e5a4f9a8fda812ab59494232c7d2\
b4deb50aa18ee9e132bfa85ac4374d7f9091abc3d015efc87\
1a584471bb1",16))
q = gmpy2.mpz(int("f4f47f05794b256174bba6e9b396a7707e563c5b",16))
g=gmpy2.mpz(int("5958c9d3898b224b12672c0b98e06c60df923cb8bc999d119\
458fef538b8fa4046c8db53039db620c094c9fa077ef389b5\
322a559946a71903f990f1f7e0e025e2d7f7cf494aff1a047\
0f5b64c36b625a097f1651fe775323556fe00b3608c887892\
878480e99041be601a62166ca6894bdd41a7054ec89f756ba\
9fc95302291",16))
a=sha.new()
a.update("For those that envy a MC it can be hazardous to your health\nSo be friendly, a matter of life and death, just like a etch-a-sketch\n")
msg="I'm YoungC in OneA"
class DSA:
    def calcR(self,k,p,q):
       r=gmpy2.f_mod(gmpy2.powmod(g,k,p),q)
       return r
    def calcS(self,k,h,x,r):
        s=gmpy2.f_mod(gmpy2.mul(gmpy2.invert(k,q),gmpy2.add(h,gmpy2.mul(x,r))),q)
        return s

def s2i(s):
  #字符串转整数
  return int(s.encode('hex'),16)

if __name__=="__main__":
    print("======g=0(mod q)=======")
    g=0
    k=147
    x1=1331
    x2=3131
    m1="Hello,world"
    m2="Goodbye,world"
    a=sha.new()
    h1=a.update(m1)
    h1=a.hexdigest()
    a=sha.new()
    h2=a.update(m2)
    h2=a.hexdigest()
    c=DSA()
    r=c.calcR(k,p,q)
    s1=gmpy2.f_mod(gmpy2.mpz(gmpy2.mul(gmpy2.invert(k,q),gmpy2.add(int(h1,16),gmpy2.mul(x1,r)))),q)
    s2=gmpy2.f_mod(gmpy2.mpz(gmpy2.mul(gmpy2.invert(k,q),gmpy2.add(int(h1,16),gmpy2.mul(x2,r)))),q)
    print "当x=1331,s等于："+str(s1)
    print "当x=3131,s等于："+str(s2)
    print "可见签名与私钥无关！"
    s3=gmpy2.f_mod(gmpy2.mul(gmpy2.mul(gmpy2.invert(k,q),(int(h1,16))),gmpy2.mul(gmpy2.invert(int(h1,16),q),int(h2,16))),q)
    s4=gmpy2.f_mod(gmpy2.mpz(gmpy2.mul(gmpy2.invert(k,q),gmpy2.add(int(h2,16),gmpy2.mul(x2,r)))),q)
    print "由hello，world的伪造的签名（s）值："+str(s3)
    print "计算goodbye，world的签名（s）值："+str(s4)
    print "伪造成功！"
    print("\n======g=1(mod q)=======")
    g=p+1
    y=gmpy2.powmod(g,k,p)
    import random
    z=random.randint(1,1301019)
    print "对任意z都成立！"
    r1=gmpy2.powmod(y,z,q)
    print "伪造hello，world的签名,r=:"+str(r1)    
    s1=gmpy2.f_mod(gmpy2.mul(r1,gmpy2.invert(z,q)),q)
    r2=c.calcR(k,p,q)
    s2=c.calcS(k,int(h1,16),x1,r2)
    w=gmpy2.invert(s2,q)
    u1 = gmpy2.f_mod(gmpy2.mul(int(h1,16),w),q)
    u2 = gmpy2.f_mod(r2 * w,q)
    v = gmpy2.f_mod((gmpy2.powmod(g, u1, p) * gmpy2.powmod(y, u2, p)) , p)
    v = gmpy2.f_mod(v,q)
    print "验证hello，world的签名,v=:"+str(v)
    if v==r1:
        print "伪造成功！"
    print "对Goodye，world同理。"
