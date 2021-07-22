import numpy as np
import pandas as pd
import secrets
import socket
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2
from utils import randMatrix, send


def setup(group):
    g1 = group.random(G1)
    g2 = group.random(G2)
    assert g1.initPP(), "ERROR: Failed to init pre-computation table for g1."
    assert g2.initPP(), "ERROR: Failed to init pre-computation table for g2."

    v = 34
    S = np.array([secrets.randbelow(2) for _ in range(v)])
    N1 = randMatrix(v, v, group)
    N2 = randMatrix(v, v, group)

    base_enc_key = (S, np.linalg.inv(N1), np.linalg.inv(N2))

    n = 34
    # next line takes a long time
    AE = np.array([(randMatrix(v, v, group), randMatrix(v, v, group)) for _ in range(n)])
    Mj1 = randMatrix(v, v, group)
    Mj2 = randMatrix(v, v, group)
    dec_key = (S, N1 * Mj1, N2 * Mj2)

    AD = AE.copy()
    for l in AD:
        l[0] *= np.linalg.inv(Mj1)
        l[1] *= np.linalg.inv(Mj2)

    return g1, g2, base_enc_key, dec_key, AE, AD


def param_encryption(params, base_enc_key, AE, group, g1):
    S, N1_inv, N2_inv = base_enc_key

    A1 = []
    A2 = []
    for l in AE:
        A1.append(l[0])
        A2.append(l[1])

    A1 = np.array(A1)
    A2 = np.array(A2)

    P1 = np.empty((params.shape[0], params.shape[1]))
    P2 = np.empty((params.shape[0], params.shape[1]))
    for r in range(params.shape[0]):
        for z in range(params.shape[1]):
            if S[z] == 0:
                x = int(params[r, z])
                if x != 0:
                    P1[r][z] = secrets.randbelow(abs(x))
                else:
                    P1[r][z] = 0
                P2[r][z] = params[r, z] - P1[r][z]
            else:
                P1[r][z] = P2[r][z] = params[r, z]

    alpha = group.random(ZR)

    X1 = np.linalg.inv(sum(A1))
    X2 = np.linalg.inv(sum(A2))

    enc_key = (X1 * N1_inv, X2 * N2_inv)
    ciphertext = []
    for i in range(params.shape[0]):
        ciphertext.append((g1 ** alpha,
                           [(g1 ** int((int(alpha) * P1[i] @ X1 @ N1_inv)[j])) for j in range(params.shape[0])],
                           [(g1 ** int((int(alpha) * P2[i] @ X2 @ N2_inv)[j])) for j in range(params.shape[0])]))

    return enc_key, ciphertext


DO_PORT = 2000
MCS_PORT = 2001
DU_PORT = 2002

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), DO_PORT))
s.listen(5)

group_name = 'MNT159'
group = PairingGroup(group_name)

g1, g2, ek, dk, AE, AD = setup(group)

print("sending group")
send(group_name, DU_PORT)
print("sending g2")
send(group.serialize(g2), DU_PORT)
print("sending key")
send(dk, DU_PORT)
print("sending ")
send(AD, DU_PORT)


params = pd.read_csv('../params.csv').drop(['b_i'], 1)
# params = params * (10 ** 6)
key, CT1 = param_encryption(params.to_numpy(), ek, AE, group, g1)

CT1_serialized = []
for i in CT1:
    ga, gp1, gp2 = i
    z = group.serialize(gp1[1])
    gp1 = [group.serialize(j) for j in gp1]
    gp2 = [group.serialize(j) for j in gp2]
    CT1_serialized.append((group.serialize(ga), gp1, gp2))

print("sending group")
send(group_name, MCS_PORT)
print("sending CT1")
send(CT1_serialized, MCS_PORT)
