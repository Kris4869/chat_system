#! -*- coding utf-8 -*-
"""
Kris Chen
ICS Final Project
Encryption module

The file acts as an ECC message encryption / decryption API
for chat state machine and server
at a ICS-student-understandable level

Workcited
Toni Mattis, python ECC Algorithm, April 13, 2013
Revised by Kris Chen

"""

import ecdsa
import eccrypt



class MyKeys(object):
    
    LEVEL = 3
    
    BITS = {i + 1 : [192, 224, 256, 384, 512][i] for i in range(5)}

    def __init__(self, owner, level = LEVEL):
        self.owner = owner
        self.bits = MyKeys.BITS[level]
        self.keypair = ecdsa.keypair(self.bits)
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


class MsgECC(object):

    def __init__(self, msg, public_key, private_key = None):
        self.msg = msg
        self.public_key = public_key
        self.private_key = private_key

    def encrypt(self):
        return eccrypt.encrypt(self.msg, self.public_key)
    
    def decrypt(self):
        return eccrypt.decrypt(self.msg, self.public_key, self.private_key)


if __name__ == "__main__":
    
    orig = "flora"
    print("Original data:")
    print(orig)
    print()
    k = MyKeys('', 1)
    qk = k.get_public_key()
    pk = k.get_private_key()
    print("Keypairs:")
    print(qk)
    print(pk)
    print()
    print("Encryption Result:")
    ECC = MsgECC(orig, qk)
    result = ECC.encrypt()
    print(result)
    print()
    print("Decryption Result:")
    nECC = MsgECC(result["msg"], result["key"], pk)
    msg = nECC.decrypt()
    print(msg)
    
