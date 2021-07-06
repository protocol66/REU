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
data = pd.read_csv('test.csv')

# TODO: compute decision function
for i in range(0, params.shape[0]):
    for j in range(0, params.shape[1]):
        params.iat[i, j] *= data.iat[i, j]

# TODO: send computed decision function to MCS


