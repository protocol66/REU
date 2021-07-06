from OU import OU, OUIntegerGroup
import pandas as pd

KEYLENGTH = 512

group = OUIntegerGroup()
ou = OU(group)

pk, sk = ou.keygen(KEYLENGTH)

# TODO: send pk to MCS and DO
# TODO: receive pk from DO
# TODO: receive params from MCS
params = pd.read_csv('params.csv')

for i in range(0, params.shape[0]):
    for j in range(0, params.shape[1]):
        params.iat[i, j] = ou.encrypt(pk, int(params.iat[i, j] * (10 ** 6)))

weights = params.drop(['b_i'], 1).copy()
intercepts = params['b_i'].copy()
data = [2, 2, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 55]  # first row of dataset

# TODO: compute decision function
for i in range(0, weights.shape[1]):
    weights['w_i_' + str(i+1)] *= data[i]  # params['w_i_1'] *= data[i]

for i in range(0, weights.shape[0]):
    for j in range(0, weights.shape[1]):
        weights.iat[i, j] = ou.decrypt(pk, sk, weights.iat[i, j])
        # weights.iat[i, j] = weights.iat[i, j].getText()
print(weights.head())

# for i in range(0, weights.shape[0]):
decision_functions = weights.sum(axis=0)
print(decision_functions.head())
# TODO: send computed decision function to MCS


