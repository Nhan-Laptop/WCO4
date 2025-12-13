from Crypto.Util.number import *

# FLAG = bytes_to_long(open('flag.txt', 'rb').read())
FLAG = bytes_to_long(b'HTB{ijeqwijeiqwjeiwjeijqwijqwijeiqwjei}')
MENU = '''
The Seers await your command:

1. Request Knowledge from the Elders
2. Consult the Seers of the Obsidian Tower
3. Depart from the Sanctum
'''
# print(FLAG)
class ChaosRelic:
    def __init__(self):
        self.p = getPrime(8)
        self.q = getPrime(8)
        self.M = self.p * self.q
        
        x0 = getPrime(15)
        self.x = x0
        print(f"The Ancient Chaos Relic fuels the Seers' wisdom. Behold its power: M = {self.M}")
        
    def next_state(self):
        self.x = pow(self.x, 2, self.M)
        
    def get_bit(self):
        self.next_state()
        return self.extract_bit_from_state()
    
    def extract_bit_from_state(self):
        return self.x % 2


class ObsidianSeers:
    def __init__(self, relic):
        self.relic = relic
        self.p = getPrime(512)
        self.q = getPrime(512)
        self.n = self.p * self.q
        self.e = 65537 
        self.phi = (self.p - 1) * (self.q - 1)
        self.d = pow(self.e, -1, self.phi)

    def sacred_encryption(self, m):
        return pow(m, self.e, self.n)

    def sacred_decryption(self, c):
        return pow(c, self.d, self.n)

    def HighSeerVision(self, c):
        return int(self.sacred_decryption(c) > self.n//2)
    
    def FateSeerWhisper(self, c):
        return self.sacred_decryption(c) % 2
    
    def divine_prophecy(self, a_bit, c):
        return self.FateSeerWhisper(c) if a_bit == 0 else self.HighSeerVision(c)
        
    def consult_seers(self, c):
        next_bit = self.relic.get_bit()
        response = self.divine_prophecy(next_bit, c)
        return response
    


def main():
    print("You stand before the Seers of the Obsidian Tower. They alone hold the knowledge you seek.")
    print("But be warned—no force in Eldoria can break their will, and their wisdom is safeguarded by the power of the Chaos Relic.")
    my_relic = ChaosRelic()
    my_seers = ObsidianSeers(my_relic)
    counter = 0

    while counter <= 1500:
        print(MENU)
        option = input('> ')

        if option == '1':
            print(f"The Elders grant you insight: n = {my_seers.n}")
            print(f"The ancient script has been sealed: {my_seers.sacred_encryption(FLAG)}")
        elif option == '2':
            ciphertext = int(input("Submit your encrypted scripture for the Seers' judgement: "), 16)
            print(f'The Seers whisper their answer: {my_seers.consult_seers(ciphertext)}')
        elif option == '3':
            print("The doors of the Sanctum close behind you. The Seers watch in silence as you depart.")
            break
        else:
            print("The Seers do not acknowledge your request.")
            continue

        counter += 1

    print("The stars fade, and the Seers retreat into silence. They shall speak no more tonight.")

if __name__ == '__main__':
    main()