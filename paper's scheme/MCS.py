from utils import *
from charm.core.math.integer import toInt, random
from OU import OU, OUIntegerGroup

KEYLENGTH = 512
DO_PORT = 2000
MCS_PORT = 2001
DU_PORT = 2002

group = OUIntegerGroup()
ou = OU(group)

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.bind((socket.gethostname(), MCS_PORT))
s.listen(5)


def Encrypted_Max(decision_functions_cipher, class_cipher, pk):
    k = len(class_cipher)

    for i in range(0, k-1):
        u = decision_functions_cipher[i] - decision_functions_cipher[i+1]
        v = u * 2
        v0 = Encrypted_LSB(v, pk)
        decision_functions_cipher[i+1] = u * (1 - v0) + decision_functions_cipher[i+1]
        class_cipher[i+1] = ((class_cipher[i] - class_cipher[i+1]) * (1 - v0)) + class_cipher[i+1]

    return class_cipher[k-1]


def Encrypted_LSB(v, other_pk):
    r = random(2 ** (KEYLENGTH-1))
    r_cipher = ou.encrypt(other_pk, r)
    s_i = v + r_cipher
    send(s_i, DO_PORT)
    SecureComparing(r, other_pk)

    B = recv(s)
    r0 = r % 2
    v0 = int(r0) ^ B
    return v0


def SecureComparing(a, other_pk):
    # print(f"a is {a}")
    a_segments = splitBits(a, 32)
    a_segments_cipher = [ou.encrypt(other_pk, i) for i in a_segments]
    # a_segments = [ciphertext(i) for i in a_segments]
    print("receiving segments")
    b_segments_cipher = recv(s)
    print(len(b_segments_cipher))
    E = []
    for i in range(0, len(b_segments_cipher)):
        E.append((b_segments_cipher[i] - a_segments_cipher[i]) * toInt(random(2 ** (KEYLENGTH-1))))
    print("sending E")
    send(E, DO_PORT)
    print("receiving i")
    i = recv(s)
    # print(a_segments[i].getText())
    compareInt(a_segments[i])


def CipherTrans(ciphertext_do, pk1, pk2):
    r = random(2 ** (KEYLENGTH - 1))
    r_cipher = ou.encrypt(pk1, r)
    send(ciphertext_do + r_cipher, DO_PORT)
    ciphertext_du = recv(s)
    r_cipher_du = ou.encrypt(pk2, r)

    return ciphertext_du - r_cipher_du


def compareInt(a):
    pk, sk = ou.keygen()
    # a = int(a)
    # print(int(a))
    # print(a.bit_length())
    R = RepNodes((32, 0), a)
    # print(len(R))
    P = [0] * 32
    for h in range(0, 32):
        for r in R:
            if r[0] == h:
                P[h] = ou.encryptWithNeg(pk, sk, -1 * r[1])
                break
            else:
                P[h] = ou.encrypt(pk, 1)
    print("send pk")
    send(pk, DO_PORT)
    # print(P)
    print("send P")
    send(P, DO_PORT)
    print("receive EPR")
    EPR = recv(s)

    result = 0  # False
    for i in EPR:
        if ou.decrypt(pk, sk, i) == 0:
            result = 1  # True

    print("send result")
    send(result, DO_PORT)


print("Receive DO_PK")
do_pk = recv(s)
print("Receive DU_PK")
du_pk = recv(s)
# do_ou = OU(group)
# do_pk, do_sk = ou.keygen()
print("Receive params")
params = recv(s, 204800)
class_label = recv(s)
# params = pd.read_csv('params.csv')
print("Send params")
send(params, DU_PORT)
print("Receive decision_functions")
decision_functions = recv(s)

print("EncryptedMax")
class_cipher = Encrypted_Max(decision_functions, class_label, do_pk)
print("CipherTrans")
result_cipher = CipherTrans(class_cipher, do_pk, du_pk)
send(result_cipher, DU_PORT)
