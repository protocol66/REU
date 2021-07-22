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

    q1 = np.empty(params.size)
    q2 = np.empty(params.size)
    for z in range(params.size):
        if S[z] == 1:
            x = int(params[z])
            if x != 0:
                q1[z] = secrets.randbelow(abs(x))
            else:
                q1[z] = 0
            q2[z] = params[z] - q1[z]
        else:
            q1[z] = q2[z] = params[z]

    beta = group.random(ZR)

    ciphertext = (g2 ** beta,
                  [[g2 ** (beta * q1 @ NM1 @ Y1)[i] for i in range(len(q1))]],
                  [[g2 ** (beta * q2 @ NM2 @ Y2)[i] for i in range(len(q2))]])

    return ciphertext
