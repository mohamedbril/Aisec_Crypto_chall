from Cryptodome.Util.number import bytes_to_long,getPrime

flag = b"CRISIS{**REDACTED**}"

Guss,Gess=(bytes_to_long(flag[len(flag)//2:]) , bytes_to_long(flag[:len(flag)//2]))

phi = 0   

def dp(res):
    if res is None:
        return None  
    uss, ess = res
    if ess == 0:
        return None  
    s = (3 * uss**2 + phi) * pow(2 * ess, -1, n) % n  
    uss_new = (s**2 - 2 * uss) % n
    ess_new = (s * (uss - uss_new) - ess) % n
    return (uss_new, ess_new)

def pd2(ress, bess):
    if ress is None:
        return bess
    if bess is None:
        return ress
    uss1, ess1 = ress
    uss2, ess2 = bess
    if uss1 == uss2:
        if ess1 != ess2:
            return None  
        else:
            return dp(ress)  
    s = (ess2 - ess1) * pow(uss2 - uss1, -1, n) % n  
    uss3 = (s**2 - uss1 - uss2) % n
    ess3 = (s * (uss1 - uss3) - ess1) % n
    return (uss3, ess3)

def da2(k, ress):
    bess = None  
    for i in reversed(range(k.bit_length())):  
        bess = dp(bess)
        if (k >> i) & 1:  
            bess = pd2(bess, ress)
    return bess



def gitPrime(bb):
    while 1==1 :
        p=getPrime(bb)
        if p%3==2:
            break
    return p

def genkeess(bb):
    p = gitPrime(bb//2)
    q = gitPrime(bb//2)
    return (0x10001,p,q)

e,p,q=genkeess(512)
d=pow(e,-1,(q-1)*(p-1))
n=p*q

b=(((Gess**2)%n)-((Guss**3)%n))%n


G=(Guss,Gess)
uss, ess = da2(e,G)

print(f"n,e,d = {(n,e,d)}")
print(f"uss = {uss}")
print(f"ess = {ess}")



# n,e,d = (4729950701539661435512408434556546492256926864155960016693444552250661382854177811484985634177901821450106900565364632504265200713358358494766215918577963, 65537, 2039803419100896457754965890807813502459031142127956695482045613626812986001856903239512849981634520791243806035627466595307384916672090763756655653454433)
# uss = 1547689769413865534366813202567974574169346868468761940437853023289581891089993697338892182491199788813133221850672663137566277684020200534491660227886319
# ess = 852413811054412600523412989144547510901118828296124616510567037313483993572357572049258980794294784201363021587613837515329948793442384344397512139393976