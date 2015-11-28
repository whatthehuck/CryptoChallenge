# -*- coding: gbk -*-

import c33 # DH
import c10 # CBC mode
import c28 # SHA1
import binascii
import random

p = 0xffffffffffffffffc90fdaa22168c234c4c6628b80dc1cd129024e088a67cc74020bbea63b139b22514a08798e3404ddef9519b3cd3a431b302b0a6df25f14374fe1356d6d51c245e485b576625e7ec6f44c42e9a637ed6b0bff5cb6f406b7edee386bfb5a899fa5ae9f24117c4b1fe649286651ece45b3dc2007cb8a163bf0598da48361c55d39a69163fa8fd24cf5f83655d23dca3ad961c62f356208552bb9ed529077096966d670c354e4abc9804f1746c08ca237327ffffffffffffffff
g = 2

print "========正常交互========="
##### normal exchange

Alice = c33.dh(random.randint(0,10000),p,g)

# A->B            Send "p", "g", "A"
Bob = c33.dh(random.randint(0,10000),p,g)
Bob_secret = Bob.shsecret(Alice.A)
print "A="+str(Alice.A)
# B->A            Send "B"
Alice_secret = Alice.shsecret(Bob.A)
print "B="+str(Bob.A)
# on Alice
print "shared key="+binascii.b2a_hex(c28.sha1(str(Alice_secret)).digest()[:16])
Alice_msg = "Alice hello OneA"
Alice_iv=''
for i in range(16):
    Alice_iv = Alice_iv+chr(random.randint(0,255))
Alice_enc = c10.cbcencrypt(Alice_msg,Alice_iv,c28.sha1(str(Alice_secret)).digest()[:16])
print "Alice发送: "+Alice_msg

# A->B            Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv

# on Bob
print "Bob收到: "+c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(Bob_secret)).digest()[:16])
Bob_msg = "Bob HELLO 1-A"
Bob_iv =''
for i in range(16):
    Bob_iv = Bob_iv+chr(random.randint(0,255))

Bob_enc = c10.cbcencrypt(Bob_msg,Bob_iv,c28.sha1(str(Bob_secret)).digest()[:16])
print "Bob发送: "+Bob_msg
# B->A            Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv

# on Alice
print "Alice收到: "+c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(Alice_secret)).digest()[:16])


print "\n\n========中间人攻击======="
print "中间人更改Alice和Bob的消息，使A=B=p="+str(p)
##### now Mallory comes into play

Alice = c33.dh(random.randint(0,10000),p,g)
# A->M            Send "p", "g", "A"
# Mallory changes A to p # A^a mod p = p^a mod p = 0
# M->B            Send "p", "g", "p"
Bob = c33.dh(random.randint(0,10000),p,g)
Bob_secret = Bob.shsecret(p)
# B->M            Send "B"
# Mallory changes B to p # B^a mod p = p^a mod p = 0
# M->A            Send "p"
Alice_secret = Alice.shsecret(p)
print "shared key="+binascii.b2a_hex(c28.sha1(str(Alice_secret)).digest()[:16])
Alice_msg = "Alice hello OneA"
Alice_iv=''
for i in range(16):
    Alice_iv = Alice_iv+chr(random.randint(0,255))
Alice_enc = c10.cbcencrypt(Alice_msg,Alice_iv,c28.sha1(str(Alice_secret)).digest()[:16])
print "Alice发送: "+str(Alice_msg)

# A->M            Send AES-CBC(SHA1(s)[0:16], iv=random(16), msg) + iv
# the secret is 0
print "攻击者解密出: "+c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(0)).digest()[:16])
# M->B            Relay that to B

print "Bob收到: "+c10.cbcdecrypt(Alice_enc,Alice_iv,c28.sha1(str(Bob_secret)).digest()[:16])
Bob_msg = "Bob HELLO OneA"
Bob_iv=''
for i in range(16):
    Bob_iv = Bob_iv+chr(random.randint(0,255))
Bob_enc = c10.cbcencrypt(Bob_msg,Bob_iv,c28.sha1(str(Bob_secret)).digest()[:16])
print "Bob发送: "+Bob_msg

# B->M            Send AES-CBC(SHA1(s)[0:16], iv=random(16), A's msg) + iv
# the secret is 0
print "攻击者解密出: "+c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(0)).digest()[:16])
# M->A            Relay that to A

# on Alice
print "Alice收到: "+c10.cbcdecrypt(Bob_enc,Bob_iv,c28.sha1(str(Alice_secret)).digest()[:16])
