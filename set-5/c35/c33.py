#!/usr/bin/env python
# -*- coding: gbk -*-
def modexp(g,u,p):
  #模指数的运算，g为底，u为指数，p为模数

  s = 1
  while u != 0:
    if u & 1:
      s = (s * g) % p
    u >>= 1
    g = ( g * g ) % p

  return s

class dh:
  #dh单方的class
  # https://en.wikipedia.org/wiki/Diffie%E2%80%93Hellman_key_exchange

  def __init__(self,a,p,g):
    self.a = a
    self.p = p
    self.A = modexp(g,a,p)

  def shsecret(self,B):
    #计算共享的密钥
    self.s = modexp(B,self.a,self.p)
    return self.s


if __name__ == "__main__":
  import random

  p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
  g = 2**16+1

  Alice = dh(random.randint(0,1318019),p,g)
  Bob = dh(random.randint(0,1318019),p,g)
  Bob_secret = Bob.shsecret(Alice.A)
  Alice_secret = Alice.shsecret(Bob.A)

  if Bob_secret == Alice_secret:
    print "OK.建立了共享密钥，共享密钥是："
  else:
    print "Something fucked up"
  #print hex(Bob_secret)
  print hex(Alice_secret)
