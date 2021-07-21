from utils import *
from random import shuffle
import pandas as pd
from charm.core.math.integer import random
from OU import OU, OUIntegerGroup


KEYLENGTH = 512
DO_PORT = 2000
MCS_PORT = 2001
DU_PORT = 2002

group = OUIntegerGroup()
ou = OU(group)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), DO_PORT))
s.listen(5)


def Encrypted_LSB(pk, sk):
    s_i_cipher = recv(s)
    s_i = ou.decrypt(pk, sk, s_i_cipher)
    s_i0 = s_i % 2

    result = SecureComparing(s_i, pk, sk)
    B = int(s_i0) ^ result
    send(B, MCS_PORT)


def SecureComparing(b, pk, sk):
    print(f"b is {b}")
    b_segments = splitBits(b, 32)
    b_segments_cipher = [ou.encrypt(pk, i) for i in b_segments]
    # b_segments = [ciphertext(i) for i in b_segments]
    print("sending segments")
    send(b_segments_cipher, MCS_PORT)
    print("receiving E")
    E = recv(s)
    j = 0
    while j < len(b_segments):
        if ou.decrypt(pk, sk, E[j]) != 0:
            break
        j += 1

    # for i in range(0, len(b_segments)):
    #     if ou.decrypt(pk, sk, E[i]) != 0:
    #         j = i
    #         break
    print("sending j")
    send(j, MCS_PORT)
    return checkInt(b_segments[j])


def CipherTrans(pk1, sk1, pk2):
    ciphertext = recv(s)
    text = ou.decrypt(pk1, sk1, ciphertext)
    ciphertext_2 = ou.encrypt(pk2, text)
    send(ciphertext_2, MCS_PORT)


def checkInt(b):
    # b = int(b)
    B = CoveringNodes((0, b), (32, 0))
    print(B)
    other_pk = recv(s)
    EP = recv(s)
    EPR = []
    print(len(EP))
    print(len(B))
    for i in range(0, len(EP)):
        r = random(2 ** (len(EP) - 1))
        EPR.append((EP[i] + ou.encrypt(other_pk, B[i][1])) * r)
    shuffle(EPR)
    send(EPR, MCS_PORT)
    return recv(s)


pk, sk = ou.keygen()

print("Sending key to MCS")
send(pk, MCS_PORT)
print("Sending key to DU")
send(pk, DU_PORT)
print("Receiving DU_PK")
du_pk = recv(s)

params = pd.read_csv('../../params.csv')

for i in range(0, params.shape[0]):
    for j in range(0, params.shape[1]):
        params.iat[i, j] = ou.encryptWithNeg(pk, sk, int(params.iat[i, j] * (10 ** 6)))

# print(sys.getsizeof(pickle.dumps(params)))

classlabels = [1, 2, 3, 4, 5, 6]
classlabels_cipher = [ou.encryptWithNeg(pk, sk, i) for i in classlabels]

print("Sending params to MCS")
send(params, MCS_PORT)
send(classlabels_cipher, MCS_PORT)

print("Encrypted_LSB")
for i in range(0,5):
    Encrypted_LSB(pk, sk)
print("CipherTrans")
CipherTrans(pk, sk, du_pk)


