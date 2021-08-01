import numpy as np
import secrets
import socket
from charm.toolbox.pairinggroup import ZR, PairingGroup
from utils import send, recv


def encryption(params, base_dec_key, AD, group, g2):
    S, NM1, NM2 = base_dec_key

    assert g2.initPP(), "ERROR: Failed to init pre-computation table for g2."

    MA1 = []
    MA2 = []
    for l in AD:
        MA1.append(l[0])
        MA2.append(l[1])

    MA1 = np.array(MA1)
    MA2 = np.array(MA2)

    Y1 = sum(MA1)
    Y2 = sum(MA2)

    q1 = np.empty(len(params))
    q2 = np.empty(len(params))
    for z in range(len(params)):
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
    # beta = 1

    ct_q1 = []
    ct_q2 = []
    for i in range(len(q1)):
        x = int(beta) * int((q1 @ NM1 @ Y1)[i])
        y = int(beta) * int((q2 @ NM2 @ Y1)[i])
        # x = int(beta) * int(q1[i])
        # y = int(beta) * int(q2[i])

        if x < -1:
            ct_q1.append((g2 ** -1) ** (-1 * x))
        else:
            ct_q1.append(g2 ** x)
        if y < -1:
            ct_q2.append((g2 ** -1) ** (-1 * y))
        else:
            ct_q2.append(g2 ** y)
    # ciphertext = (g2 ** beta,
    #               [g2 ** int((int(beta) * q1 @ NM1 @ Y1)[i]) for i in range(len(q1))],
    #               [g2 ** int((int(beta) * q2 @ NM2 @ Y2)[i]) for i in range(len(q2))])

    ciphertext = (g2 ** beta, ct_q1, ct_q2)
    return ciphertext


# DO_PORT = 2000
# MCS_PORT = 2001
# DU_PORT = 2002
#
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# s.bind((socket.gethostname(), DU_PORT))
# s.listen(5)
#
# print("receiving group")
# group_name = recv(s)
# group = PairingGroup(group_name)
# print("receiving g2")
# g2 = group.deserialize(recv(s))
# print("receiving key")
# base_description_key = recv(s)
# print("receiving AD")
# AD = recv(s)
#
# patient_data = [2, 2, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 55]  # first row of dataset
# # patient_data = [2,1,2,3,1,3,0,3,0,0,0,1,0,0,0,1,2,0,2,0,0,0,0,0,2,0,2,3,2,0,0,2,3,26]
#
# CT2 = encryption(patient_data, base_description_key, AD, group, g2)
#
#
# gb, gq1, gq2 = CT2
# gq1 = [group.serialize(i) for i in gq1]
# gq2 = [group.serialize(i) for i in gq2]
# CT2_serialized = (group.serialize(gb), gq1, gq2)
#
# signal = recv(s)
# print("sending CT2")
# send(CT2_serialized, MCS_PORT)
#

