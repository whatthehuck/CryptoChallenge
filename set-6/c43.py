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
        s=gmpy2.f_mod(gmpy2.mpz(gmpy2.mul(gmpy2.invert(k,q),gmpy2.add(h,gmpy2.mul(x,r)))),q)
        return s
def s2i(s):
  #字符串转整数
  return int(s.encode('hex'),16)

if __name__=="__main__":
    b=DSA()
    h=s2i(a.digest())
    for k in range(2**16):
        r=b.calcR(k,p,q)
        #s=b.calcS(k,h,x,r)
        if r==548099063082341131477253921760299949438196259240:
            s=857042759984254168557880549501802188789837994940
            print "found!"
            x=gmpy2.divm((gmpy2.mul(s,k)-h),r,q)
            print "因为k很小，爆破即得k值，解得x为:"
            print str(x)
            c=sha.new()
            c.update(hex(x)[2:])
            print "x的sha1值为"+c.hexdigest()
            print "与题设0954edd5e0afe5542a4adf012611a91912a3ec16相同"
    print "finish"
        
