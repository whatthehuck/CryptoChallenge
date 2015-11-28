#coding:utf8
#!/usr/bin/env python

from rsa import RSA
from i2s import i2s, s2i
import base64
import math
from decimal import *


class oracle:

	def __init__(self):
		self.rsa = RSA()
		self.pub, self.private = self.rsa.keygen(l=512)

	def getPubKey(self):
		return self.pub

	def isEven(self, num):
		return ord(self.rsa.decrypt(num, self.private)[-1]) & 1 == 0


def attack(enc, key, isEven):
	e = key[0]
	n = key[1] #去 从公钥中去值

	m1 = s2i(enc[0])  #将加密信息的第一位转成整数
	m2 = pow(2, e, n)   # (2**e)%n)
	m1 = (m1 * m2) % n
	limit = int(math.log(n, 2)) + 1
	getcontext().prec = limit

	a = Decimal(0)
	b = Decimal(n)
	for x in range(limit):
		t = (a+b)/2
		#如果倍增后的明文是偶数，加倍所述明文未包裹模---模数是素数。这意味着明文是不到一半的模量。
		if isEven([i2s(m1)]):
			b = t
		else:
			a = t
		m1 = (m1 * m2) % n

	return i2s(int(b)).encode('string_escape')
		


if __name__ == "__main__":

	msg = "VGhhdCdzIHdoeSBJIGZvdW5kIHlvdSBkb24ndCBwbGF5IGFyb3VuZCB3aXRoIHRoZSBGdW5reSBDb2xkIE1lZGluYQ=="


	myoracle = oracle()
	pub = myoracle.getPubKey()

	rsa = RSA()
	enc = rsa.encrypt(base64.b64decode(msg), pub)
	returnmeg = attack(enc, pub, myoracle.isEven)
	print returnmeg

