from Cryptodome.Util.number import bytes_to_long,getPrime

flag = b"CRISIS{**REDACTED**}"

Gx,Gy=(bytes_to_long(flag[len(flag)//2:]) , bytes_to_long(flag[:len(flag)//2]))

a = 0   

def point_double(P):
    if P is None:
        return None  
    x, y = P
    if y == 0:
        return None  
    s = (3 * x**2 + a) * pow(2 * y, -1, n) % n  
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

def double_and_add(k, P):
    Q = None  
    for i in reversed(range(k.bit_length())):  
        Q = point_double(Q)
        if (k >> i) & 1:  
            Q = point_add(Q, P)
    return Q



def gitPrime(bb):
    while 1==1 :
        p=getPrime(bb)
        if p%3==2:
            break
    return p

def genkey(bb):
    p = gitPrime(bb//2)
    q = gitPrime(bb//2)
    return (0x10001,p,q)

e,p,q=genkey(512)
d=pow(e,-1,(q-1)*(p-1))
n=p*q

b=(((Gy**2)%n)-((Gx**3)%n))%n


G=(Gx,Gy)
x, y = double_and_add(e,G)

print(f"n,e,d = {(n,e,d)}")
print(f"x = {x}")
print(f"y = {y}")

