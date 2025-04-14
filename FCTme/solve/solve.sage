from random import randint
from Crypto.Util.number import long_to_bytes


def factor(n, e, d):
    while True:
        z = randint(2, n - 2)
        k, x = 0, e * d - 1
        while not int(x) & 1:
            k += 1
            x /= 2
        t = Integer(z).powermod(x, n)
        if t == 1 or t == (n-1):
            continue
        bad_z = False
        for _ in range(k):
            u = pow(t, 2, n)
            if u == -1 % n:
                bad_z = True
                break
            if u == 1:
                p = gcd(n, t-1)
                q = gcd(n, t+1)
                return p, q
            else:
                t = u
        if bad_z:
            continue


n,e,d = (6683198205910169075517410697882860490850643696358436730839677807110695219436120979577259214987740553169615246943889945593287260962972081163097055750715523, 65537, 5904713760422608907635147041205903092935667210129279064128810657569473507957340205314376953686364369370834277139537212229934180214088584277123847719103113)
Cx = 4235163152446689647944278009659612349426470110501825646457368145009125560426475320570320075466282057314136948664431797447129766187422042697339630400301514
Cy = 235304632776458431414392277762053289085293149373589352428231972188991210572612756797554125422429042542258285610094079212916988482861895909890184040415189


(p, q) = factor(n, e, d)
assert p * q == n
assert p % 3 == 2
assert q % 3 == 2
phin = (p - 1) * (q - 1)
assert (e * d - 1) % phin == 0
k = (e * d - 1) / phin


b = (pow(Cy, 2, n) - pow(Cx, 3, n)) % n
EC = EllipticCurve(Zmod(n), [0, b])
assert EC.is_on_curve(Cx, Cy)
E1 = EllipticCurve(IntegerModRing(p), [0, b % p])
E2 = EllipticCurve(IntegerModRing(q), [0, b % q])
C = EC(Cx, Cy)


E_order = E1.order() * E2.order()
einv = inverse_mod(e, E_order)


G = einv * C
Gx, Gy = G.xy()

flag = long_to_bytes(int(Gy)) + long_to_bytes(int(Gx))
print(flag)




