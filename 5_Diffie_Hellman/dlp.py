from Crypto.Util.number import getPrime
from sage.all import * 
from sage.misc.prandom import randrange
from math import isqrt
p = getPrime(16)
F = GF(p)
g = F.multiplicative_generator()
# print(g.multiplicative_order())
x = randrange(1, p) 
y = g**x 
# print("p =", p)
# print("g =", g)
# print("y =", y) 
# print("x =", x) 
def brute_dlp(g,y,p): 
    for i in range(p):
        if g**i == y:
            return i
    return None
x_ = brute_dlp(g,y,p)
# print("Brute-force DLP solution x_ =", x_)
# print(x==x_)
def floor_div(a,b):
    return a//b 
def ceil_div(a,b): 
    return floor_div(a,b) + (a%b > 0)
def bsgs_dlp(g,y,p, order = None):
    if order is None:
        n = g.multiplicative_order()
    else:
        n = order
    m = ceil_div(isqrt(n),1) + 1 
    table = {}
    baby_step = 1
    for i in range(m):
        table[baby_step] = i 
        baby_step = (baby_step * g) % p 

    lamb = pow(g, n - m, p) 
    giant_step = y 
    for j in range(m):
        if giant_step in table:
            return j*m + table[giant_step]
        giant_step = (giant_step * lamb) % p
    return None 

x__ = bsgs_dlp(g,y,p)
# print("BSGS DLP solution x__ =", x__)

def lin_congruence(a,b,m): 
    '''
    return x satisfy the modular equation ax = b modulo m
    '''
    a = a % m 
    b = b % m 
    u = 0 
    v = 0 
    d, u, v = xgcd(a,m) 
    if b % d != 0:
        return None 
    x0 = (u*(b//d)) % m
    if (x0 < 0):
        x0 += m 
    sol = [(x0+i*(m//d)) for i in range(d)]
    return sol 

def pollard_rho_dlp(g,y,p):
    n = g.multiplicative_order()
    def step(beta, x, d): 
        r = ZZ(beta) % 3 
        if r == 0:
            beta = (beta * g) % p 
            x = (x+1) % n
        elif r == 1:
            beta = (beta * beta) % p 
            x = (2 * x) % n 
            d = (2 * d) % n 
        else: 
            beta = (beta * y) % p 
            d = (d + 1)% n 
        return beta, x , d
    while True:
        x0 = randrange(1,n)
        d = 0 
        beta = pow(g, x0,p)
        slow = (beta, x0, d)
        fast = step(*slow)
        fast = step(*fast)
        while slow[0] != fast[0]: 
            slow = step(*slow)
            fast = step(*fast)
            fast = step(*fast)
        a = (fast[2] - slow[2]) % n
        b = (slow[1] - fast[1]) % n
        if a == 0:
            continue 
        sol = lin_congruence(a,b,n)
        if sol is not None:
            for s in sol:
                if pow(g,s,p) == y:
                    return s

x_rho = pollard_rho_dlp(g,y,p)
# print("Pollard's Rho DLP solution x_rho =", x_rho)

'''

'''
p = 257
F = GF(p)
g = F.multiplicative_generator()
# print(g.multiplicative_order())
x = randrange(1, p)
h = g**x 
def dlp_2adic(g,h,p, e = None):
    '''
    solve the dlp on the group of order 2^k
    '''
    if e is not None:
        n = 2**e
        k = e
    else:
        n = g.multiplicative_order()
        print(f"n = {n}")
        k = n.valuation(2)
    x = ""
    for i in range(1,k+1):
        val = pow(h, n//(2**i),p)
        if val == 1:
            x += "0"
            # c0 =0 
            h = h 
        else:
            x += "1"
            # c0 = 1 
            # precompute h for next step
            mul = pow(g, 2**(i-1), p) 
            h = h * pow(mul, p-2, p) % p 
    return Integer(x[::-1],2)
x_ = dlp_2adic(g,h,p)
# print("2-adic DLP solution x_ =", x_)
# print(x == x_)
# def floor_div(a,b):
#     return a//b 
# def ceil_div(a,b): 
#     return floor_div(a,b) + (a%b > 0)
# def bsgs_dlp(g,y,p):
#     n = g.multiplicative_order()
#     m = ceil_div(isqrt(n),1) + 1 
#     table = {}
#     baby_step = 1
#     for i in range(m):
#         table[baby_step] = i 
#         baby_step = (baby_step * g) % p 

#     lamb = pow(g, n - m, p) 
#     giant_step = y 
#     for j in range(m):
#         if giant_step in table:
#             return j*m + table[giant_step]
#         giant_step = (giant_step * lamb) % p
#     return None 

def dlp_padic(g,h, p, q, e = None): 
    '''
    solve the dlp on the group of order p^k
    '''
    if e is not None:
        n = q**e
        k = e
    else:
        n = g.multiplicative_order()
        k = n.valuation(q)
    x = 0 
    b_j = h 
    alpha = pow(g, n//q, p)
    for j in range(k):
        h_i = pow(b_j, n//(q**(j+1)), p)
        a_j = bsgs_dlp(alpha, h_i, p, order = q)
        assert a_j >=0 and a_j < q 
        x += a_j * (q**j)
        mul = pow(g, a_j * (q**j), p)
        assert gcd(mul, p)==1
        b_j = (b_j * pow(mul, p-2, p)) % p
    return x 

def pohlig_hellman(g,h,p, facs = None):
    '''
    solve the dlp on the group of order n
    where n = p1^k1 * p2^k2 * ... * pt^kt
    '''
    n = g.multiplicative_order()
    if facs is not None:
        factorization = facs
    else:
        factorization = n.factor()
    x_list = []
    mod_list = []
    for (q, e) in factorization:
            g_sub = pow(g, n // (q**e), p)
            h_sub = pow(h, n // (q**e), p)
            
            if q == 2:
                xi = dlp_2adic(g_sub, h_sub, p, e)
            else:
                xi = dlp_padic(g_sub, h_sub, p, q, e)
                
            x_list.append(xi)
            mod_list.append(q**e)
            
    return crt(x_list, mod_list)

n = "575ccba5eb432070f54b12237b91996ff33d9e8fd7c8766da0833a89fd1d95abda573a9e6973c7769f60de749cd044a5d50c62f929680eeb44c0b93b014c1bfdbf668f581a2bfa034c09b2f6b755f8ffe883b5b4e756621b983967e64d728f09f1e8485672b896550928bcab85e72569d140e8e2ddf79dde58a6f6bbcae9c4ae6e8b93e4dc882e0da5ab78a07a92b4257564b34a64b7b19d91f1dac8e695f9b988c49063d72a891762c08683bdee592ff7ce8bd5906a671ea8ea5a54c65211a7182f628e5aa87ad3d388be3fae703ed8c43df264c33dd4c8d6faf3d8571b5c220c05f14093a72b93fe0d93d73b1440fdad30e310daa87e566219b82217d0895d"
c = "307652ee5a77dab4e70ded15e2c791c268e2c2e389d1f02887ea5baf8cf2b4aab98b4c9c47556a3c4b98c668a90d856c548c574dfa9e252fb92c1886d0fb54ef2492de80879ed5c655ed7e3edebb748599ce2f5d6efaf3843818571d96c92a072f8d7d246c7f440001b5b9e75d6736bb96549e35b45f8e2ba7c133d9238b997c0a6c88a8748e086432017566a372b3defe3c070d0f68694eb3e3c1dd4d12942769d619ec214b6ec1a2d269b81363f5f4866ea8558bb10b22659069001083f45445031a9612df9cf9ee8cc905529e98b4d8c079fd1876d3f03b49c16f2105d3ca5fd9e0b14e777a678d6951aa9c92a35313ce444320e57b17e034ee6278926345"

n = Integer(n,16)
c = Integer(c,16)
print(n)

p = 99780657006850307217163612271973390190663607819917363361274107729126350596004575425605962244848758942414685363499768407969467515520576830928375995814136925441205578035494602110292472739632571208253734744415405389058270558553966428927961144743641000259884783893427233387123259437508145503920189935184380947127
q = 110527350987883845703818360205139695189371692715336120000550661421700243956585990933562072789588327968698648424408232508707836774937738833785305269946638572818303754817202929468530110527537160908746219153021943572111734050046799583587771499425306849674104694050784670115941207695741101581323717208164212189323
assert p * q == n 
cp = c % p
cq = c % q
g=3
Fp = GF(p)
Fq = GF(q)
print(factor(p-1))
xp = pohlig_hellman(
    g = Fp(g),
    h = Fp(cp),
    p = p,
    facs = factor(p-1)
)
xq = pohlig_hellman(
    g = Fq(g),
    h = Fq(cq),
    p = q,
    facs = factor(q-1)
)
FLAG = crt(
    [xp, xq],
    [p-1, q-1]
)
flag_hex = hex(FLAG)[2:]
if len(flag_hex) % 2:
    flag_hex = "0" + flag_hex
print(bytes.fromhex(flag_hex))
