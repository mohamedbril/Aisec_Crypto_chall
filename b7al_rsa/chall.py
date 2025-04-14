from Cryptodome.Util.number import *
from sympy.ntheory import sqrt_mod
import os
from math import gcd
from functools import reduce


flag = b"CRISIS{i_g07_c0nfu53d_15_7h47_r54_hmmm_1n73r3571ng_9467AX1}"


p=getPrime(1024)
q=getPrime(512)
n=p*q
e=0x10001

def crt(remainders, moduli):
    M = reduce(lambda a, b: a * b, moduli)
    x = 0
    for ai, ni in zip(remainders, moduli):
        Mi = M // ni
        inv = pow(Mi, -1, ni)
        x += ai * Mi * inv
    return x % M

def point_double(P):
    if P is None:
        return None  
    x, y = P
    if y == 0:
        return None  
    s = (3 * x**2 + p) * pow(2 * y, -1, n) % n  
    x_new = (s**2 - 2 * x) % n
    y_new = (s * (x - x_new) - y) % n
    return (x_new, y_new)

def point_add(P, Q):
    if P is None:
        return Q
    if Q is None:
        return P
    x1, y1 = P
    x2, y2 = Q
    if x1 == x2:
        if y1 != y2:
            return None  
        else:
            return point_double(P)  
    s = (y2 - y1) * pow(x2 - x1, -1, n) % n  
    x3 = (s**2 - x1 - x2) % n
    y3 = (s * (x1 - x3) - y1) % n
    return (x3, y3)

def scalar_multiplication(k, P):
    Q = None  
    for i in reversed(range(k.bit_length())):  
        Q = point_double(Q)
        if (k >> i) & 1:  
            Q = point_add(Q, P)
    return Q


def is_quadratic_residue(x, A, B, p):
    f = (x**3 + A * x + B) % p
    return pow(f, (p - 1) // 2, p) == 1


def generate_valid_point(flag, p, q):
    flag_len = len(flag)
    total_bytes = 192 
    A = p
    B = q    
    while True:
        pad = os.urandom(total_bytes - flag_len)
        candidate = flag + pad
        x_candidate = int(bytes_to_long(candidate))
        valid_p = is_quadratic_residue(x_candidate, A, B, p)
        valid_q = is_quadratic_residue(x_candidate, A, B, q)
        if valid_p and valid_q:
            rhs_p = (x_candidate**3 + A * x_candidate + B) % p
            rhs_q = (x_candidate**3 + A * x_candidate + B) % q
            y_p = int(sqrt_mod(rhs_p, p))
            y_q = int(sqrt_mod(rhs_q, q))
            y = crt([y_p, y_q], [p, q])
            return x_candidate, y

x,y=generate_valid_point(flag,p,q)

C=scalar_multiplication(e,(x,y))

print(f"n = {n}")
print(f"xx,yy = {C}")




