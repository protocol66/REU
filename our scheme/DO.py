import numpy as np
import pandas as pd
import secrets
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2
from utils import randMatrix


def setup(group):
    g1 = group.random(G1)
    g2 = group.random(G2)
    assert g1.initPP(), "ERROR: Failed to init pre-computation table for g1."
    assert g2.initPP(), "ERROR: Failed to init pre-computation table for g2."

    v = 34
    S = np.array([group.random(ZR) for _ in range(v)])
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


def encryption(params, base_enc_key, AE, group, g1):
    S, N1_inv, N2_inv = base_enc_key

    A1 = []
    A2 = []
    for l in AE:
        A1.append(l[0])
        A2.append(l[1])

    A1 = np.array(A1)
    A2 = np.array(A2)

    # TODO: change df to numpy
    P1 = P2 = np.empty((params.shape[0], params.shape[1]))
    for r in range(params.shape[0]):
        for z in range(params.shape[1]):
            if S[z] == 0:
                P1[r][z] = secrets.randbelow(params.iat[r, z] * (10 ** 6)) / (10 ** 6)
                P2[r][z] = params.iat[r, z] - P1[r][z]
            else:
                P1[r][z] = P2[r][z] = params.iat[r, z]

    alpha = group.random(ZR)

    X1 = np.linalg.inv(sum(A1))
    X2 = np.linalg.inv(sum(A2))

    enc_key = (X1 * N1_inv, X2 * N2_inv)
    ciphertext = np.empty(6)
    for i in range(params.shape[0]):
        ciphertext[i] = (g1 ** alpha, g1 ** (alpha * P1[i] * X1 * N1_inv), g1 ** (alpha * P2[i] * X2 * N2_inv))

    return enc_key, ciphertext


group = PairingGroup('MNT159')

g1, g2, ek, dk, AE, AD = setup(group)

params = pd.read_csv('../params.csv').drop(['b_i'], 1)
encryption(params, ek, AE, group, g1)


