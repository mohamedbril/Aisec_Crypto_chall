#!/usr/bin/env python
EncEnc
m = 3

# Generate test data set
scale_factor = 1
p_size = int(1000 * scale_factor)
l_size = int(55 * scale_factor)
d_size = int(105 * scale_factor)
M = 2^l_size

N, e = (42630939979180229081499803612410641780723320525892930648423575933146265958976301645533162893256024406357806756080281663100000739748137110464115463096818815116225288709411725433831721223507852973860167389356024573949700272944866485142579021009933304733613300016046142296373130921608499163462929609014058275685470637573744728313752418581382196989828624235367474430465061237517348174061017944762366460079299502488606925876018747337520636546469206590030202138445462192346969878156406175949517826725642845325077346947376478093377918057135040484672706341969623148375553938696754408803367416127957401038462143, 24072222660875178367385039031587858040732497044181727323747431170776667749973891280414140638764661298310493212054613897180480020001833106560017511962067402554848365172454287038110213547162908181018140156000279247197953409385470511201960067027126519065068238819695881660645356220654624263044599051106120616841218190222057068498315858760363773470303373569548926629619288269505190636831492950899928162825369775179338184227626527491452039617284816861897303790908119948156123584132686131994003663811756015769964145075371014986991076781236804038616930374491838004161088315666658501011179311009032336138703247)
dp_tilde, dq_tilde = (9835725266356621, 20585528271707263)

def nearest_below(x):
	c = floor(x)
	if not (c < x):
		c -= 1
	return c


Enc
############# PARAMETERS #################
delta = float((d_size - l_size) / int(N).bit_length())
beta = float((d_size) / int(N).bit_length())
alpha = float((int(e).bit_length()) / int(N).bit_length())
sigma = .35
tau = float(max(1/2, 1 - 2*beta))

X = int(e*2^(d_size - p_size))
Y = int(2^p_size)

print(f'beta: {float(beta)}')
print(f'(beta - delta)/beta: {float((beta - delta)/beta)}')
print(f'sigma: {sigma}')
print(f'delta: {delta}')

P.<xp, xq, yp, yq, zp, zq> = PolynomialRing(ZZ, 6, order = 'lex')
index_map = {g:i for i,g in enumerate(P.gens())}


Enc
######################## HELPER DATA #########################
import itertools
M_sigma = [(a,b,c) for a, c, b in itertools.product(range(m + 1), range(m + 1), range(nearest_below(2*sigma*m) + 1))]

M_1 = [(a,b,c) for c in range(m + 1) for a in range(c + 1) for b in range(c - a + 1)]
M_2 = [(a,b,c) for c in range(m + 1) for a in range(c + 1, m + 1) for b in range(a - c)]
M_3 = [(a,b,c) for a in range(m + 1) for c in range(m + 1) for b in range(a + c + 1) if ((a,b,c) not in M_1 and (a,b,c) not in M_2 and (a + b + c) % 2 == 0)]
M_4 = [(a,b,c) for a in range(m + 1) for c in range(m + 1) for b in range(a + c + 1) if ((a,b,c) not in M_1 and (a,b,c) not in M_2 and (a,b,c) not in M_3)]
MM = [(a,b,c) for a in range(m + 1) for c in range(m + 1) for b in range(a + c + 1)]

M_tilde = [(a,b,c) for a, c, b in itertools.product(range(m + 1), range(m + 1), range(2*m + 1))]

# Sort M_sigma
M_tilde.sort(key = lambda p: xp^p[0]*yp^p[1]*zp^p[2])
M_sigma.sort(key = lambda p: xp^p[0]*yp^p[1]*zp^p[2])
MM.sort(key = lambda p: xp^p[0]*yp^p[1]*zp^p[2])

def E_f(a,b,c):
	if (a,b,c) in M_1:
		return 0
	elif (a,b,c) in M_2:
		return b
	elif (a,b,c) in M_3:
		return (a + b - c)//2
	elif (a,b,c) in M_4:
		return (a + b - c + 1)//2
	else:
		return a


def E_g(a, b, c):
	if (a,b,c) in M_1:
		return b
	elif (a,b,c) in M_2:
		return 0
	elif (a,b,c) in M_3:
		return (-a + b + c)//2
	elif (a,b,c) in M_4:
		return (-a + b + c - 1)//2
	else:
		return c

def E_h(a, b, c):
	if (a,b,c) in M_1:
		return a
	elif (a,b,c) in M_2:
		return c
	elif (a,b,c) in M_3:
		return (a - b + c)//2
	elif (a,b,c) in M_4:
		return (a - b + c - 1)//2
	else:
		return 0

def E_x(a, b, c):
	if (a,b,c) in M_1:
		return 0
	elif (a,b,c) in M_2:
		return a - b - c
	elif (a,b,c) in M_3:
		return 0
	elif (a,b,c) in M_4:
		return 0
	else:
		return 0

def E_z(a, b, c):
	if (a,b,c) in M_1:
		return -a - b + c
	elif (a,b,c) in M_2:
		return 0
	elif (a,b,c) in M_3:
		return 0
	elif (a,b,c) in M_4:
		return 1
	else:
		return 0

def trans(F):
	ypi = index_map[yp]
	yqi = index_map[yq]
	xpi = index_map[xp]
	zpi = index_map[zp]
	xqi = index_map[xq]
	zqi = index_map[zq]

	F = P(F)

	# Replace all instances of yp*yq by N
	new_dict = {}
	for t, v in F.dict().items():
		num = min(t[ypi], t[yqi])
		new_t = list(t)
		new_t[ypi] -= num
		new_t[yqi] -= num
		new_t = tuple(new_t)

		if new_t not in new_dict:
			new_dict[new_t] = 0

		new_dict[new_t] += int(N)^num * int(v)
	F = P(new_dict)

	# Step 2
	F_ = P(0)
	for t, v in F.dict().items():
		if t[ypi] != 0:
			F_ += P({t: v})
			continue

		new_t = list(t)
		xp_pow = t[xpi]
		zp_pow = t[zpi]
		new_t[xpi] = 0
		new_t[zpi] = 0
		new_t = tuple(new_t)

		mm = P({new_t: int(v)})
		F_ += mm*(xq + 1)^xp_pow*(zq - 1)^zp_pow
	F = F_

	# Step 3
	F_ = P(0)
	for t, v in F.dict().items():
		if t[ypi] == 0:
			F_ += P({t: int(v)})
			continue

		new_t = list(t)
		xq_pow = t[xqi]
		zq_pow = t[zqi]
		new_t[xqi] = 0
		new_t[zqi] = 0
		new_t = tuple(new_t)

		mm = P({new_t: v})
		F_ += mm*(xp - 1)^xq_pow*(zp + 1)^zq_pow
	F = F_

	return F

def lambda_abc(a, b, c):
	if b % 2 == 0:
		return xq^a*yq^(b//2)*zq^c
	else:
		return xp^a*yp^((b + 1)//2)*zp^c

# Highest monomial in the (zp, xp, yp) ordering
def highest_monomial(p):
	monomials = p.monomials()
	monomials.sort(key = lambda g: g(xp, xp, yp, yp, zp, zp))

	return monomials[-1]

# Rescale a poly to make the determinant of lattice smaller
def rescale_poly(poly):
	g = gcd(N - 1, e*M)

	monomials = poly.monomials()
	highest = highest_monomial(poly)

	d = int(poly[highest])
	t = next(iter(highest.dict().keys()))

	Xpow = t[index_map[xp]] + t[index_map[xq]] + t[index_map[zp]] + t[index_map[zq]]
	Ypow = t[index_map[yp]] + t[index_map[yq]]
	xy_pow = X^Xpow * Y^Ypow
	assert d % xy_pow == 0
	d //= xy_pow

	E4 = 0
	while d % N == 0:
		E4 += 1
		d //= N
	E5 = 0
	while d % (N - 1) == 0:
		E5 += 1
		d //= N - 1

	new_d = int(d) * int(g)^E5 * int(xy_pow)

	multiplier = pow(int(N), E4, (e*M)^(2*m))*pow(int((N - 1)//g), E5, (e*M)^(2*m))
	multiplier = pow(int(multiplier), -1, (e*M)^(2*m))

	p = P(0)
	for mm in monomials:
		if mm == highest:
			p += new_d * mm
		else:
			p += int(poly[mm]) * int(multiplier) * mm

	return p


Enc
################ PKE SHIFT POLYS #################
f_tilde = xp*yp - xq - e*dp_tilde
g_tilde = yp*zp - N*zq + e*dq_tilde*yp
h_tilde = N*xp*zq - xq*zp - e^2*dp_tilde*dq_tilde - e*dp_tilde*zp - e*dq_tilde*xq

def p_tilde(a, b, c):
	res = f_tilde^E_f(a, b, c)*g_tilde^E_g(a, b, c)*h_tilde^E_h(a, b, c)*xp^E_x(a, b, c)*zp^E_z(a, b, c)*(e*M)^(2*m - E_f(a, b, c) - E_g(a, b, c) - E_h(a, b, c))
	return P(res)

def pke_row(a, b, c):
	if (a,b,c) in MM:
		return trans(p_tilde(a, b, c)*yq^(b//2))(X*xp, X*xq, Y*yp, Y*yq, X*zp, X*zq)
	else:
		if b % 2 == 0:
			return trans(p_tilde(a, b, c)*yq^((a + c)//2)*yq^((b - a - c + 1)//2))(X*xp, X*xq, Y*yp, Y*yq, X*zp, X*zq)
		else:
			return trans(p_tilde(a, b, c)*yq^((a + c)//2)*yp^((b - a - c + 1)//2))(X*xp, X*xq, Y*yp, Y*yq, X*zp, X*zq)


Enc
################# TLP SHIFT POLYS #####################
f = M*(xp*yp - xq)
g = M*(yp*zp - N*zq)
h = M*(N*xp*zq - xq*zp)

def p(a, b, c):
	res = f^E_f(a, b, c)*g^E_g(a, b, c)*h^E_h(a, b, c)*xp^E_x(a, b, c)*zp^E_z(a, b, c)*(e*M)^(2*m - E_f(a, b, c) - E_g(a, b, c) - E_h(a, b, c))
	return P(res)

def p_ast(a, b, c, i, y):
	return trans(p(a, b, c)*yq^(b//2)*y^i)(X*xp, X*xq, Y*yp, Y*yq, X*zp, X*zq)

def tlp_row(a, b, c):
	return trans(p(a, b, c)*yq^(b//2))(X*xp, X*xq, Y*yp, Y*yq, X*zp, X*zq)


Enc
############ FETCH SHIFT POLYS ##################
# PKE polys
PKE_polys = []
for t in M_sigma:
	PKE_polys.append(pke_row(*t))

# TLP polys
TLP_polys = []
for t in MM:
	TLP_polys.append(tlp_row(*t))
	a, b, c = t
	if b == a + c:
		for i in range(1, floor(tau*b) - b//2 + 1):
			TLP_polys.append(p_ast(a, b, c, i, yq))
		for i in range(1, floor(tau*b) - (b + 1)//2 + 1):
			TLP_polys.append(p_ast(a, b, c, i, yp))

# Filter out un-needed tlp polys
for i in range(len(TLP_polys) - 1, -1, -1):
	p = TLP_polys[i]
	
	mm = highest_monomial(p)
	mm = next(iter(mm.dict().keys()))
	if mm[index_map[yq]] + mm[index_map[yp]] <= sigma*m:
		TLP_polys.pop(i)



Enc
############## COMBINE BOTH #################
shift_polys = PKE_polys + TLP_polys
# Rescale them for LLL
shift_polys = list(map(rescale_poly, shift_polys))

# Sort the monomials
monomials = set()
for p in shift_polys:
	monomials |= set(p.monomials())
monomials = list(monomials)
monomials.sort(key = lambda q: q(xp, xp, yp, yp, zp, zp))

# Build the coeff matrix
B = [[0 for _ in range(len(monomials))] for __ in range(len(shift_polys))]
for i, p in enumerate(shift_polys):
	for j, mm in enumerate(monomials):
		B[i][j] = p[mm]

B = matrix(ZZ, B)


Enc
############### APPLY COPPERSMITH TECHNIQUE TO FINISH ################
print(f'dim: {B.nrows()}')
B = B.LLL()
print('Finished LLL')
B = B.change_ring(QQ)

# Rescale columns back
for i, mm in enumerate(monomials):
	t = next(iter(mm.dict().keys()))
	Xpow = t[index_map[xp]] + t[index_map[xq]] + t[index_map[zp]] + t[index_map[zq]]
	Ypow = t[index_map[yp]] + t[index_map[yq]]
	d = X^Xpow * Y^Ypow

	assert all(map(lambda j: int(B[j][i]) % d == 0, range(B.nrows())))

	B.rescale_col(i, 1/d)

# Look at ideal gen by rows
P = P.change_ring(QQ)
H = Sequence([], P)
monomials = vector(P, monomials)

save((B, monomials), 'LLL_result.sobj')

amount = 40
for h in list(B*monomials)[:amount]:
	H.append(h)

print('Solving variety')
I = H.ideal()
roots = []
for root in I.variety(ring = ZZ):
	roots.append(root)
print(roots)

for root in roots:
	p = int(root[yp])
	if N % p == 0 and p != 1 and p != N:
		print(f'p: {p}')


Enc
from Crypto.Util.number import long_to_bytes


Enc
p=6572135861721070317358439703621000766832999219422796700090117934182886046283685721159555983464487687194845902060719422264892033777661418335590118069446676810145334767463641461975966354559598872819764602453297279208855742410922915335180383156416128049801168055260906288675504584465345003953983415274883
q=6486618791233616101765757686277677366397878718883658891388742061391212462601505895731262213011667108994985332679489763865289664299081821338236780266262870917469008750197326606077425045936252263554987099901275485836943676725766997074122517565210878935588904748820368399165164320215928621212923733011221


Enc
enc=33142150992086052749746398837498441840798580866858734478515232477271336725419328506999030057620162108354820981792117325744616712875552093879777471426523074415822876526820761573661083529325428130982359530564207056191152879805199218154173005708150254592221642114731484565221664796070209257079083041122061935418263310456931620267411563607851982388461329632311957874537218735018302348145858954356684077536582979836299362861935969704544825351302077986614711011323894430937045472707646830623521538432269978588704047723793183452347365971785607011792904180254139617566430550911075065173279067474909810010716842


Enc
d=pow(e,-1,(p-1)*(q-1))


Enc
m=long_to_bytes(pow(enc,d,N))


Enc
m


Enc


