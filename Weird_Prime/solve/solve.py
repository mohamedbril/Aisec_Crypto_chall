from Cryptodome.Util.number import *

chunk_size = 64

a = 0xaa0c3dab7d5fbbf1
b = inverse(a, 1 << 64)
n = 0x35151869037a57dd6747e1d4f06c5867a953ce50de3655a7d692fd3daaa82f451c72c3cb7f922951991b53f026fba8e7195a8c577ab578c77ebf1afeb73cc57b6652d780c159ecd29cb9dc23d48dc2ffc68d4744b7f27d8eebab076d3f8a08533061624a3d840dd32efee5d6f6420a46c64742401573493245e75b5cfb83e6eeb39b5a8da652eb90bef056e10c4d371987c8503183de3aba38f7d22d3fd9a63a5c20d26d585594573117e2aaa3271c39c5192fdc86d25eeef151504b061aa8d0fa6ce361fae3b306dac7b1c5bc5b08d03fc6b4cf86fca8e62cc532b24c7934e58d0477691fbab58409961eb8058bb2ae3847539d58e3a4323cc621da0b1bea4b
e = 0x10001
c = 0x2f6bc3a487881f3e1e9f262e0f19ea63dbfcdf4565013da249e9f7d7bca64ca4a5b2a4d9cbd561ae24d90e7bf72990aa044f688e7c8989e1c4ac504c73f585104b84fa87d7866ca24a3e42bab1a2eef32dd601c51a8edcfaf943979dd3e98488904b6873ceb7da415bf37c62b8b318c2725bc33d880595a94d4dcd46b7bbd2b2ec714777434b80653e129b8cd97f6ba58227df0537b82ac68b35a24a33662cfc005fe48c69fc00ae887414f0c5c7e25bfd5ad419d41fd7340bde5146edebee869c822163f1c21b4b1cc3e3658ce56914d7ab9153e9345ef00d80c9e88859ce02316a68165fdab60e7afe066244ac2702fb8beab68a8ad6a7690d1c901abf20c1

chunk_size = 64
cmod = 1 << chunk_size

def get_chunks(n, bits):
  narr = []
  for i in range(bits // chunk_size):
    narr.append((n >> (i * chunk_size)) % (1 << chunk_size))
  return narr

narr = get_chunks(n, 2048)

pqlower = narr[0]
pqupper = (narr[1] - 2 * narr[0] * b) % cmod

print('P*Q=', (pqupper << chunk_size) + pqlower)

# PQ=1032214371490704807906446342100871755

# factors = [3,3,5,7,17,53,227,2659,366419,1079830789,15228483979] use factordb.com to get the factors

pqfact = [3,3,5,7,17,53,227,2659,366419,1079830789,15228483979]

print (f'Factors found: {pqfact}')

possible_pqs = set()

for i in range(2 ** len(pqfact)):
    use = '{{:0{}b}}'.format(len(pqfact)).format(i)
    assert len(use) == len(pqfact), len(use)
    pq = [1, 1]
    for j in range(len(pqfact)):
        pq[int(use[j])] *= pqfact[j]
    p, q = pq
    possible_pqs.add(tuple(sorted(pq)))


def getlowercase(U):
    u = 0
    mult = U
    for i in range(16):
        u += (mult << (i * chunk_size))
        mult = (mult * b) % (1 << chunk_size)
    return u

for P, Q in possible_pqs:
    p = getlowercase(P)
    q = getlowercase(Q)
    if p * q == n:
        print('p: {}'.format(getlowercase(P)))
        print('q: {}'.format(getlowercase(Q)))
        d = inverse(e, (p - 1) * (q - 1))
        print('Flag: {}'.format(long_to_bytes(pow(c, d, n)).decode()))
        exit(0)