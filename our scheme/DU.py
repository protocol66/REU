import numpy as np
import pandas as pd
import secrets
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2


def encryption(params, base_dec_key, AD, group, g2):
    S, NM1, NM2 = base_dec_key

    MA1 = []
    MA2 = []
    for l in AD:
        MA1.append(l[0])
        MA2.append(l[1])

    MA1 = np.array(MA1)
    MA2 = np.array(MA2)

    Y1 = sum(MA1)
    Y2 = sum(MA2)

    params = params.to_numpy()

    q1 = q2 = np.empty(params.size)
    for z in range(params.size):
        if S[z] == 1:
            q1[z] = secrets.randbelow(params[z] * (10 ** 6)) / (10 ** 6)
            q2[z] = params[z] - q1[z]
        else:
            q1[z] = q2[z] = params[z]

    beta = group.random(ZR)

    ciphertext = (g2 ** beta, g2 ** (beta * NM1  * Y1 * q1), g1 ** (beta * NM2 * Y2 * q2))

    return ciphertext
