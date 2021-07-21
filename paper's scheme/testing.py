import sys
# from MCS import *
import socket
from utils import *


#
# msg = 5
# msg2 = -1000
#
# group = OUIntegerGroup()

# ou = OU(group)
#
# pk, sk = ou.keygen(bitLength=512)
#
# start = datetime.now()
# msg_cipher = ou.encryptWithNeg(pk, sk, msg)
# end = datetime.now()
# print("Encryption:", end-start)
# msg2_cipher = ou.encryptWithNeg(pk, sk, msg2)
#
# cipher_add = msg_cipher + msg2_cipher
# cipher_mul = msg_cipher * msg2
#
# start = datetime.now()
# decrypted = ou.decrypt(pk, sk, msg_cipher)
# end = datetime.now()
# print("Decryption:", end-start)
# #
# add_decrypt = ou.decrypt(pk, sk, cipher_add)
# mul_decrypt = ou.decrypt(pk, sk, cipher_mul)
# print("Add: ", add_decrypt)
# print("Mul: ", mul_decrypt)

# tree = PBT(32)
# print(tree.is_perfect(tree.root, tree.root.h+1))
# sum = 0
# for i in range(0, 33):
#     sum += 2 ** i
# print(sum)
# n = Node(25, 0)
# print(sys.getsizeof(n))

print(splitBits(0xFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFFF, 32))