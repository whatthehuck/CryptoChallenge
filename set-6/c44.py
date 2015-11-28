# -*- coding: gbk -*-
import sha
import gmpy2

y = gmpy2.mpz(int("2d026f4bf30195ede3a088da85e398ef869611d0f68f07\
13d51c9c1a3a26c95105d915e2d8cdf26d056b86b8a7b8\
5519b1c23cc3ecdc6062650462e3063bd179c2a6581519\
f674a61f1d89a1fff27171ebc1b93d4dc57bceb7ae2430\
f98a6a4d83d8279ee65d71c1203d2c96d65ebbf7cce9d3\
2971c3de5084cce04a2e147821",16))
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

def i2s(i):
  #整数转字符串 
  x = hex(i).replace("0x","").replace("L","")
  if len(x) % 2 == 1:
    x = "0" + x
  return x.decode('hex')

def s2i(s):
  #字符串转整数
  return int(s.encode('hex'),16)

class DSA:
    def calcR(self,k,p,q):
       r=gmpy2.f_mod(gmpy2.powmod(g,k,p),q)
       return r
    def calcS(self,k,h,x,r):
        s=gmpy2.f_mod(gmpy2.mpz(gmpy2.mul(gmpy2.invert(k,q),gmpy2.add(h,gmpy2.mul(x,r)))),q)
        return s
def s2i(s):
  #字符串转整数
  return int(s.encode('hex'),16)

if __name__=="__main__":
    print "首先，我们选择两个有着同样r值的签名，这说明他们公用了一个k值"
    m1=gmpy2.mpz(int("a4db3de27e2db3e5ef085ced2bced91b82e0df19",16))
    m2=gmpy2.mpz(int("d22804c4899b522b23eda34d2137cd8cc22b9ce8",16))
    s1=gmpy2.mpz(1267396447369736888040262262183731677867615804316)
    s2=gmpy2.mpz(1021643638653719618255840562522049391608552714967)
    r1=gmpy2.mpz(1105520928110492191417703162650245113664610474875)
    k=gmpy2.divm((m1-m2),(s1-s2),q)
    c=DSA()
    print "用式k=(m1-m2)/(s1-s2)(mod q)"
    print "求得k="+str(k)
    R1=c.calcR(k,p,q)
    if r1==R1:
        print "k校验正确！"
    
