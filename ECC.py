#ICS Final Project, Elliptic-curve Cryptography module
#@Kris Chen

from os import urandom
from random import randint

from elliptic import mulp
#Finite Field Elliptic-curve math, (Cite: R. Hirschfeld)

from protocol import Rabbit
#Message <-> Coordinates protocol, (Cite: T. Mattis)


class Curves(object):

    DOMAINS = {
    # Bits : (p, order of E(GF(P)), parameter b, base point x, base point y)
    192 : (0xfffffffffffffffffffffffffffffffeffffffffffffffff,
           0xffffffffffffffffffffffff99def836146bc9b1b4d22831,
           0x64210519e59c80e70fa7e9ab72243049feb8deecc146b9b1,
           0x188da80eb03090f67cbf20eb43a18800f4ff0afd82ff1012,
           0x07192b95ffc8da78631011ed6b24cdd573f977a11e794811),
    
    224 : (0xffffffffffffffffffffffffffffffff000000000000000000000001,
           0xffffffffffffffffffffffffffff16a2e0b8f03e13dd29455c5c2a3d,
           0xb4050a850c04b3abf54132565044b0b7d7bfd8ba270b39432355ffb4,
           0xb70e0cbd6bb4bf7f321390b94a03c1d356c21122343280d6115c1d21,
           0xbd376388b5f723fb4c22dfe6cd4375a05a07476444d5819985007e34),

    256 : (0xffffffff00000001000000000000000000000000ffffffffffffffffffffffff,
           0xffffffff00000000ffffffffffffffffbce6faada7179e84f3b9cac2fc632551,
           0x5ac635d8aa3a93e7b3ebbd55769886bc651d06b0cc53b0f63bce3c3e27d2604b,
           0x6b17d1f2e12c4247f8bce6e563a440f277037d812deb33a0f4a13945d898c296,
           0x4fe342e2fe1a7f9b8ee7eb4a7c0f9e162bce33576b315ececbb6406837bf51f5),

    384 : (0xfffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffeffffffff0000000000000000ffffffff,
           0xffffffffffffffffffffffffffffffffffffffffffffffffc7634d81f4372ddf581a0db248b0a77aecec196accc52973,
           0xb3312fa7e23ee7e4988e056be3f82d19181d9c6efe8141120314088f5013875ac656398d8a2ed19d2a85c8edd3ec2aef,
           0xaa87ca22be8b05378eb1c71ef320ad746e1d3b628ba79b9859f741e082542a385502f25dbf55296c3a545e3872760ab7,
           0x3617de4a96262c6f5d9e98bf9292dc29f8f41dbd289a147ce9da3113b5f0b8c00a60b1ce1d7e819d7a431d7c90ea0e5f),

    521 : (0x1ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff,
           0x1fffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffa51868783bf2f966b7fcc0148f709a5d03bb5c9b8899c47aebb6fb71e91386409,
           0x051953eb9618e1c9a1f929a21a0b68540eea2da725b99b315f3b8b489918ef109e156193951ec7e937b1652c0bd3bb1bf073573df883d2c34f1ef451fd46b503f00,
           0x0c6858e06b70404e9cd9e3ecb662395b4429c648139053fb521f828af606b4d3dbaa14b5e77efe75928fe1dc127a2ffa8de3348b3c1856a429bf97e7e31c2e5bd66,
           0x11839296a789a3bc0045c8a5fb42c7d1bd998f54449579b446817afbd17273e662c97ee72995ef42640c550b9013fad0761353c7086a272c24088be94769fd16650)
    }

    CURVE_P = 3

    def __init__(self, bits):
        self.bits = bits
    
    def get_curve(self):
        p, n, b, x, y = Curves.DOMAINS[self.bits]
        return self.bits, p, n, Curves.CURVE_P, p - b, (x, y)
    

class MyKeys(object):

    def __init__(self, owner):
        self.owner = owner
        self.bits = 256
        self.keypair = self.gen_keypair(self.bits)
        self.public_key = self.keypair[0]
        self.private_key = self.keypair[1]

    def get_owner(self):
        return self.owner

    def get_bits(self):
        return self.bits

    def get_keypair(self):
        return self.keypair

    def get_public_key(self):
        return self.public_key

    def get_private_key(self):
        return self.private_key

    def randkey(self, bits, n):
        rb = urandom(int(bits / 8) + 8)  
        c = 0
        for r in rb:
            c = (c << 8) | r
        return (c % (n - 1)) + 1

    def gen_keypair(self, bits):
        bits, cn, n, cp, cq, g = Curves(self.bits).get_curve()
        d = self.randkey(bits, n)
        q = mulp(cp, cq, cn, g, d)
        return (bits, q), (bits, d)


class MsgECC(object):

    def __init__(self, msg, public_key, private_key = None):
        self.msg = msg
        self.public_key = public_key
        self.private_key = private_key


    def encrypt(self, encrypter = Rabbit):
        bits, q = self.public_key
        bits, cn, n, cp, cq, g = Curves(bits).get_curve()
        k = randint(1, n - 1)        
        kg = mulp(cp, cq, cn, g, k)         
        sg = mulp(cp, cq, cn, q, k)         
        return encrypter(sg[0]).encrypt(self.msg), kg
    
    def decrypt(self, decrypter = Rabbit):
        bits, d = self.private_key
        kg = self.public_key
        bits, cn, n, cp, cq, g = Curves(bits).get_curve()
        sg = mulp(cp, cq, cn, kg, d)    
        return decrypter(sg[0]).decrypt(self.msg)

if __name__ == "__main__":
    
    orig = "I love you"
    print("Original data:")
    print(orig)
    print()
    k = MyKeys('')
    qk = k.get_public_key()
    pk = k.get_private_key()
    print("Public Key:")
    print(qk)
    print("Private Key:")
    print(pk)
    print()
    print("Encryption Result:")
    ECC = MsgECC(orig, qk)
    result = ECC.encrypt()
    print(result[0])
    print()
    print("Decryption Result:")
    nECC = MsgECC(result[0], result[1], pk)
    msg = nECC.decrypt()
    print(msg)
    
