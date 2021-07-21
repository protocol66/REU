from utils import *
from OU import OU, OUIntegerGroup

KEYLENGTH = 512
DO_PORT = 2000
MCS_PORT = 2001
DU_PORT = 2002

group = OUIntegerGroup()
ou = OU(group)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), DU_PORT))
s.listen(5)


pk, sk = ou.keygen(KEYLENGTH)

# receive pk from DO
print("Receive DO_PK")
do_pk = recv(s)

# send pk to MCS and DO
print("Sending key to MCS")
send(pk, MCS_PORT)
print("Sending key to DO")
send(pk, DO_PORT)

# receive params from MCS
print("Receive params")
params = recv(s, 204800)
# params = pd.read_csv('params.csv')

# for i in range(0, params.shape[0]):
#     for j in range(0, params.shape[1]):
#         params.iat[i, j] = ou.encryptWithNeg(pk, sk, int(params.iat[i, j] * (10 ** 6)))

weights = params.drop(['b_i'], 1).copy()
intercepts = params['b_i'].copy()
# patient_data = [2, 2, 0, 3, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 3, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 1, 0, 55]  # first row of dataset
patient_data = [2,1,2,3,1,3,0,3,0,0,0,1,0,0,0,1,2,0,2,0,0,0,0,0,2,0,2,3,2,0,0,2,3,26]

for i in range(0, weights.shape[1]):
    weights['w_i_' + str(i+1)] *= patient_data[i]  # params['w_i_1'] *= data[i]

# for i in range(0, weights.shape[0]):
#     for j in range(0, weights.shape[1]):
#         weights.iat[i, j] = ou.decrypt(pk, sk, weights.iat[i, j])
# print(weights.head())

decision_functions = weights.join(intercepts).sum(axis=1)

print("Send decision functions")
send(decision_functions, MCS_PORT)
print("Receive result")
result_cipher = recv(s)
result = ou.decrypt(pk, sk, result_cipher)
print(result)


