from Cryptodome.Util.number import *
from os import urandom

flag = b"CRISIS{**REDACTED**}"

def GD(a, b):
    if 0 == b:
        return 1, 0, a
    x, y, q = GD(b, a % b)
    x, y = y, (x - a // b * y)
    return x, y, q

def g_val(pp, dd, ll):
    while True:
        p = getPrime(pp)
        q = getPrime(pp)
        if GCD(p - 1, q - 1) == 2:
            break
    d_p = getPrime(dd)
    d_q = getPrime(dd)
    s, t, g = GD(p - 1, q - 1)
    if s < 0:
        s += q - 1
    else:
        t += p - 1
    n = p * q
    phi = (p - 1) * (q - 1)
    e = (inverse(d_p, p - 1) * t * (q - 1) + inverse(d_q, q - 1)  * s * (p - 1)) // g % phi
    return (n, e), (d_p % (2**ll), d_q % (2**ll))
    
def Enc(m, pub):
    n, e = pub
    return pow(m, e, n)

pp , dd ,ll = (1000 , 105 ,55)
pub, lsb_dp_dq = g_val(pp, dd, ll)
flag_momala7 = urandom(2 * pp // 8 - len(flag) - 1) + flag
enc = Enc(int(flag_momala7.hex(), 16), pub)
print(f"enc = {enc}")
print(f"lsb_dp_dq = {lsb_dp_dq}")
print(f"pub = {pub}")

