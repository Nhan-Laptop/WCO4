from Crypto.Util.number import *
from math import prod
import random

class RAS(object):
    def __init__(self, arr):
        self.n = prod(arr)*prod(arr)
        
    def generate_e(self):
        e = random.getrandbits(4048)
        return e
    
    def encrypt(self, pt):
        e = self.generate_e()
        assert self.n.bit_length() == 4048
        c = [pow(m, e, self.n) for m in pt]
        return  c
        
flag = b'KMACTF{???????????????????????????????}'
flag1, flag2, flag3 = bytes_to_long(flag[:len(flag)//3]), bytes_to_long(flag[len(flag)//3:2*len(flag)//3]), bytes_to_long(flag[2*len(flag)//3:])

# shuffle it
m1 = flag3
m2 = 65537*flag1**2 + flag3*flag2**2 

menu = '''
Welcome to my RAS stolen from tvd2004
1. Send primes
2. Get encrypted flag
'''

while True : 
    print(menu)
    choose = input('> ')
    if choose == '1':
        
        try:
            count = int(input(f"Not 1, not 2, you can choose number prime in RSA system : "))
        except :
            exit()
            
        arr = []
        for i in range(count) :
            p = int(input(f"Prime {i} : "))
            arr.append(p)
        
        ras =  RAS(arr)
        
    elif choose == '2':
        
        print("Here is ciphertext :")
        print(ras.encrypt([m1,m2]))
        
    else:
        raise Exception("Invalid choice!!!")
