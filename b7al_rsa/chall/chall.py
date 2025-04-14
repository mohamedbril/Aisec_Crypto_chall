from Cryptodome.Util.number import *
from sympy.ntheory import sqrt_mod
from functools import reduce
import os

flag = b"CRISIS{**REDACTED**}"


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


def qudra_res(x, A, B, p):
    f = (x**3 + A * x + B) % p
    return pow(f, (p - 1) // 2, p) == 1


def gen_point(flag, p, q):
    flag_len = len(flag)
    total_bytes = 192 
    A = p
    B = q    
    while True:
        pad = os.urandom(total_bytes - flag_len)
        candidate = flag + pad
        x_candidate = int(bytes_to_long(candidate))
        valid_p = qudra_res(x_candidate, A, B, p)
        valid_q = qudra_res(x_candidate, A, B, q)
        if valid_p and valid_q:
            rhs_p = (x_candidate**3 + A * x_candidate + B) % p
            rhs_q = (x_candidate**3 + A * x_candidate + B) % q
            y_p = int(sqrt_mod(rhs_p, p))
            y_q = int(sqrt_mod(rhs_q, q))
            y = crt([y_p, y_q], [p, q])
            return x_candidate, y

x,y=gen_point(flag,p,q)

C=scalar_multiplication(e,(x,y))

print(f"n = {n}")
print(f"xx,yy = {C}")

'''

n = 1996105034947741262418384507512336404602624401837369063325777224528437089579434552686361610097866983798741528798163393029634143194784069032160208400569269602142318650111625924942629785698502567190436918594883279705073894851324256968344478303750642379130929066894377471874365218378298735564635901585652755373256479714984895439810385910980574413872604134345484749747291080909367209478390179860468975146466397375109501140877021972335548639707672237129788233208437927
xx,yy = (1732470247240165786616922211747767877178736079354782842450923550557701035762021252090542003969822492690406005068932050823445366310204584699661700128337935010644944880861992818742416609637476890548118418828589055688065226721503216588599763276784821614013546229018312155236608370321937655848152220054615627672581391427041978442363267645652210543500181056745279161606102133071105661119060593719422532747232502483881425317189745378829028063596083537589652438340407169, 1740427973984732707326583228434142560489301012096938021900327329001264033227068764219022607601379440513726574159564580931010600324227246451186190725705676008842654439636099558810651777792391650062984275775169771608029933567858844303821981645089265955668310600694445093866652091562799680384284576257406609966749137264395023143957140105559701519872451270620017368269260291744970609443108978214888726034803184744810862873918853323901314944508501237152129718771437031)

'''