from OU import OU, OUIntegerGroup
from charm.core.math.integer import random
import pandas as pd
from random import shuffle

KEYLENGTH = 512

group = OUIntegerGroup()
ou = OU(group)

pk, sk = ou.keygen()

# TODO: receive pk from DO,DU
# TODO: receive params from DO
params = pd.read_csv('params.csv')
# TODO: send params to DU
# TODO: receive decision functions from DU


# TODO: Encrypted_Max
def Encrypted_Max(decision_functions_cipher, class_cipher):
    k = len(class_cipher)

    for i in range(0, k-1):
        u = decision_functions_cipher[i] - decision_functions_cipher[i+1]
        v = u * 2
        v0 = Encrypted_LSB(v)
        decision_functions_cipher[i+1] = u * (1 - v0) + decision_functions_cipher[i+1]
        class_cipher[i+1] = ((class_cipher[i] - class_cipher[i+1]) * (1 - v0)) + class_cipher[i+1]

    return class_cipher[k]


def Encrypted_LSB(v):
    r = random(2 ** (KEYLENGTH-1))
    r_cipher = ou.encrypt(do_pk, r)
    s = v + r_cipher
    # TODO: send s to DO
    SecureComparing(r)
    # TODO: receive B from DO
    r0 = r % 2
    v0 = r0 ^ B
    return v0


def SecureComparing(a):
    a_segments = split_bits(a, 32)
    # TODO: Receive b segments from DO
    for i in range(0,len(b_segments)):
        E = (b_segments[i] - a_segments[i]) * randm


# node is a tuple (h, o)
def RepNodes(node, a):
    if node[0] <= 0:
        return []

    leftNode = (node[0] - 1, 2 * node[1])
    rightNode = (node[0] - 1, 2 * node[1] + 1)

    if (node[1] + 1) * (2 ** node[0]) - 1 == a:
        return [node]

    if (rightNode[1] * (2 ** rightNode[0])) <= a < ((rightNode[1] + 1) * (2 ** rightNode[0])):
        return [leftNode] + RepNodes(rightNode, a)

    return RepNodes(leftNode, a)


def CoveringNodes(node, root):
    if node[0] == root[0]:
        return [root]
    elif node[1] % 2 == 0:
        parent = (node[0] + 1, node[1] // 2)
    else:
        parent = (node[0] + 1, (node[1] - 1) // 2)

    return [node] + CoveringNodes(parent, root)


def compareInt(a, b):
    R = RepNodes((32, 0), a)
    P = [0] * 32
    for h in range(0, 32):
        for r in R:
            if r[0] == h:
                P[h] = ou.encryptWithNeg(pk, sk, -1 * r[1])
                break
            else:
                P[h] = ou.encrypt(pk, 1)
    # TODO: send P to DO
    EPR = checkInt(b)
    result = False
    for i in EPR:
        if ou.decrypt(pk, sk, i) == 0:
            result = True

    return result


def checkInt(b, EP):
    B = CoveringNodes((0, b), (32, 0))
    # TODO: receive EP from MCU
    EPR = [0] * 32
    for i in range(0, 32):
        r = random(2 ** (KEYLENGTH - 1))
        EPR[i] = (EP[i] + ou.encrypt(pk, B[i])) * r
    shuffle(EPR)
    # TODO: send EPR to MCU and wait for result
    return result


def split_bits(value, n):
    ''' Split `value` into a list of `n`-bit integers '''
    mask = (1 << n) - 1
    segments = []
    while value:
        segments.append(value & mask)
        value >>= n
    segments.reverse()
    return segments
