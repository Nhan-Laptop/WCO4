from Crypto.Util.number import getPrime
from sage.all import * 
from sage.misc.prandom import randrange
from math import isqrt
p = getPrime(16)
F = GF(p)
g = F.multiplicative_generator()
print(g.multiplicative_order())
x = randrange(1, p) 
y = g**x 
print("p =", p)
print("g =", g)
print("y =", y) 
print("x =", x) 
def brute_dlp(g,y,p): 
    for i in range(p):
        if g**i == y:
            return i
    return None
x_ = brute_dlp(g,y,p)
print("Brute-force DLP solution x_ =", x_)
print(x==x_)
def floor_div(a,b):
    return a//b 
def ceil_div(a,b): 
    return floor_div(a,b) + (a%b > 0)
def bsgs_dlp(g,y,p):
    n = g.multiplicative_order()
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
print("BSGS DLP solution x__ =", x__)

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
print("Pollard's Rho DLP solution x_rho =", x_rho)


'''

'''
p = 257
F = GF(p)
g = F.multiplicative_generator()
print(g.multiplicative_order())
x = randrange(1, p)
h = g**x 
def dlp_2adic(g,h,p):
    '''
    solve the dlp on the group of order 2^k
    '''
    n = g.multiplicative_order()
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
print("2-adic DLP solution x_ =", x_)
print(x == x_)
def dlp_padic(g,h, p, q): 
    '''
    solve the dlp on the group of order p^k
    '''
    n = g.multiplicative_order()
    k = n.valuation(q)
    assert p - 1 == q**k 
    x = 0 
    b_j = h 
    alpha = pow(g, n//q, p)
    for j in range(k):
        h_i = pow(b_j, n//(q**(j+1)), p)
        a_j = bsgs_dlp(alpha, h_i, p)
        assert a_j >=0 and a_j < q 
        x += a_j * (q**j)
        mul = pow(g, a_j * (q**j), p)
        assert gcd(mul, p)==1
        b_j = (b_j * pow(mul, p-2, p)) % p
    return x 

def pohlig_hellman(g,h,p):
    '''
    solve the dlp on the group of order n
    where n = p1^k1 * p2^k2 * ... * pt^kt
    '''
    n = g.multiplicative_order()
    factorization = n.factor()
    x_list = []
    mod_list = []
    for (q, e) in factorization:
        if q == 2:
            x_q = dlp_2adic(g,h,p)
            x_list.append(x_q)
            mod_list.append(2**e)
            continue
        x_q = dlp_padic(g,h,p,q)
        x_list.append(x_q)
        mod_list.append(q**e)
    x = crt(x_list, mod_list)
    return x
