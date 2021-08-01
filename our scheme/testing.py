import math

import numpy as np
import pandas as pd
import numpy
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, G2
from charm.core.math.integer import integer
from utils import randMatrix, solve_dlog_bsgs
from DO import setup, param_encryption
from DU import encryption
from MCS import decision_function


group1 = PairingGroup("MNT159")
# group2 = PairingGroup("MNT159")
#
g1 = group1.random(G1)
g2 = group1.random(G2)
#
# x = g1 ** (-1) ** 100
# y = g2 ** (450)
#
# w = g1 ** 2
# z = g2 ** 3
# # print(x < y)
# q = group1.pair_prod(x, y)
# e = group1.pair_prod(w, z)
#
# print(int(q))
#
# print(solve_dlog_bsgs(g1, x, group1.order()))


a = np.array([1, 3, 4, 6])
b = np.array([8, 5, 3, 2])
# b *= (10 ** 3)

c = group1.random(ZR)
d = group1.random(ZR)
# c = 500
# d = 100
#
M = randMatrix(4, 4, group1)
# M = [[6, 6, 4, 7], [2, 5, 8, 9], [1, 4, 2, 5], [1, 2, 3, 4]]
N = np.linalg.inv(M)
N = N.T


# N = 1 / M
#
# for i in range(4):
#     for j in range(4):
#         if math.isinf(N[i][j]):
#             N[i][j] = 0

cta = []
ctb = []

sum = 0
sum1 = 0
for i in range(len(a)):
    x = int((int(c) * (a @ M)[i]))
    y = int((int(d) * (b @ N)[i]))
    sum += (x * y)
    sum1 += (a @ M)[i] * (b @ N)[i]

    if x < -1:
        cta.append((g1 ** -1) ** (-1 * x))
    else:
        cta.append(g1 ** x)
    if y < -1:
        ctb.append((g2 ** -1) ** (-1 * y))
    else:
        ctb.append(g2 ** y)

Eq = 1
for i in range(len(cta)):
    Eq *= group1.pair_prod(cta[i], ctb[i])

e = group1.pair_prod(g1 ** int(c), g2 ** int(d))

print(f"numpy:{np.dot(a,b)}")
print(f"sum:{sum / (int(c) * int(d))}")
print(f"sum1:{sum1}")
print(f"pairing:{solve_dlog_bsgs(e, Eq, 100000000)}")

exit()

group_name = 'MNT159'
group = PairingGroup(group_name)

g1, g2, ek, dk, AE, AD = setup(group)

params = pd.read_csv('../params.csv').drop(['b_i'], 1)
params = params * (10 ** 3)
# params = abs(params)
key, CT1 = param_encryption(params.to_numpy(), ek, AE, group, g1)

patient_data = [2, 2, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 55]  # first row of dataset
# patient_data = [2,1,2,3,1,3,0,3,0,0,0,1,0,0,0,1,2,0,2,0,0,0,0,0,2,0,2,3,2,0,0,2,3,26]

CT2 = encryption(patient_data, dk, AD, group, g2)
decision_functions = []
for i in range(6):
    print(int(numpy.dot(params.to_numpy()[i], patient_data)))
for i in CT1:
    decision_functions.append(decision_function(i, CT2, 10000000, group))


print(decision_functions)

