from Cryptodome.Util.number import bytes_to_long , isPrime
import random

ss= 64

cc=0xaa0c3dab7d5fbbf1

def next_prime(n):
   
    while cc:
        p=[]
        sp=random.getrandbits(ss)

        for i in range(n // ss):
            p.append(sp)
            sp=cc*sp % 2**ss

        pp=p[0]
        for i in range(1,len(p)):
            pp= (pp << ss) + p[i]

        if isPrime(pp):
            return pp    
            

e=0x10001
n=next_prime(1024) * next_prime(1024)

flag = b"CRISIS{**REDACTED**}"

pt=bytes_to_long(flag)

ct=pow(pt,e,n)

print(f"n = {hex(n)}")
print(f"e = {hex(e)}")
print(f"ct = {hex(ct)}")