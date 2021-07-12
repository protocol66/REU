from charm.core.math.integer import *
from charm.toolbox.PKEnc import PKEnc


class OUIntegerGroup:
    def __init__(self):
        self.p = 0
        self.q = 0
        self.n = 0

    def setParam(self, p, q):
        if isPrime(p) and isPrime(q):
            self.p = p
            self.q = q
            self.n = (self.p ** 2) * self.q
            return True
        else:
            print("p and q are not primes")
        return False

    def __str__(self):
        return f"p = {self.p} \n " \
               f"q = {self.q} \n"

    def paramGen(self, bits):
        self.p = randomPrime(bits, 1)
        self.q = randomPrime(bits, 1)
        self.n = (self.p ** 2) * self.q
        return self.p, self.q, self.n

    # random generator
    def randomGen(self):
        while True:
            g = random(self.n - 1)
            g_p = pow(g % (self.p ** 2), self.p - 1, self.p ** 2)
            if (g_p != 1) and (g % self.p != 0) and (g % self.q != 0):
                break
        return g

    # random number in group
    def random(self, max=0):
        if max == 0:
            return random(self.n)
        else:
            return random(max)


# class to contain encrypted text and override operators
class ciphertext():
    def __init__(self, c):
        self.c = c

    # [[m + n]] = [[m]] * [[n]]
    def __add__(self, other):
        if type(other) == ciphertext:
            return ciphertext(self.c * other.c)

    # [[a * m]] = [[m]]^a
    # 'other' has to be plaintext value
    def __mul__(self, other):
        if type(other) == int or type(other) == integer:
            return ciphertext(self.c ** other)

    def __sub__(self, other):
        if type(other) == ciphertext:
            return ciphertext(self.c * (other.c ** -1))

    # return encrypted text
    def getText(self):
        return self.c


# Okamoto-Uchiyama cryptosystem
class OU(PKEnc):
    def __init__(self, groupObj):
        PKEnc.__init__(self)
        self.group = groupObj

    def keygen(self, bitLength=512):
        p, q, n = self.group.paramGen(bitLength)
        g = self.group.randomGen()
        h = pow(g % n, n, n)  # g^n % n

        pk = {'n': n, 'g': g, 'h': h, 'l': bitLength}
        sk = {'p': p, 'q': q}

        return pk, sk

    def encrypt(self, pk, m):
        r = self.group.random(pk['n'])
        C = (((pk['g'] % pk['n']) ** m) * ((pk['h'] % pk['n']) ** r)) % pk['n']  # g^m * h^r % n
        return ciphertext(C)

    def encryptWithNeg(self, pk, sk, m):
        neg = False
        if m < 0:
            m *= -1
            neg = True

        C = self.encrypt(pk, m)

        if neg:
            C *= toInt(sk['p']) - 1

        return C

    def decrypt(self, pk, sk, cipher):
        p = sk['p']
        C = cipher.getText()

        def L(x):
            x = toInt(x) - 1
            if x != 0:
                return x / p
            else:
                return 0

        a = L(pow(C % (p ** 2), p - 1, p ** 2)) % p
        if a == 0:
            return 0
        b = L(pow(pk['g'] % (p ** 2), p - 1, p ** 2)) % p
        m = toInt((a / b) % p)

        if m > (int(p) // 2):
            m -= p/2

        return m


