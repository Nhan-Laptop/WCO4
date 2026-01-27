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
