import socket
import pickle
import numpy as np
import secrets
import math
from charm.toolbox.pairinggroup import ZR, pair


def send(data, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # print(f"Sending to {port}")
    s.connect((socket.gethostname(), port))
    s.send(pickle.dumps(data))
    s.close()


def recv(s, size=1024):
    client, addr = s.accept()
    # print(f"Connection from {client} , {addr}")
    data = []
    while True:
        packet = client.recv(4096)
        if not packet:
            break
        data.append(packet)
    data = pickle.loads(b"".join(data))
    # data = client.recv(size)
    client.detach()
    return data


def randMatrix(row, col, group):
    # return np.array([[float(int(group.random(ZR))) for _ in range(col)] for _ in range(row)])
    return np.array([[float(secrets.randbelow(100)) for _ in range(col)] for _ in range(row)])

def adjugate_matrix(matrix):
    adj_matrix = matrix.copy()
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            adj_matrix[i,j]

# Taken from https://github.com/kevinlewi/fhipe/blob/master/fhipe/ipe.py
def solve_dlog_bsgs(g, h, dlog_max, rec_cnt=0):
    # Attempts to solve for the discrete log x, where g^x = h, using the Baby-Step
    # Giant-Step algorithm. Assumes that x is at most dlog_max.

    if rec_cnt > 1:
        return 0
    # alpha = int(math.ceil(math.sqrt(dlog_max))) + 1
    # g_inv = g ** -1
    # tb = {}
    # for i in range(alpha + 1):
    #     tb[(g ** (i * alpha)).__str__()] = i
    #     for j in range(alpha + 1):
    #         s = (h * (g_inv ** j)).__str__()
    #         if s in tb:
    #             i = tb[s]
    #             return i * alpha + j
    # return -1

    m = int(math.ceil(math.sqrt(dlog_max)))

    tbl = {g ** i: i for i in range(m)}

    g_inv = (g ** -1) ** m
    y = h
    for i in range(m):
        if y in tbl:
            return i * m + tbl[y]
        # if (g ** i) * (h ** -1)  g ** 0:
        #     return i
        y *= g_inv

    return -1 * solve_dlog_bsgs(g ** -1, h, dlog_max, rec_cnt+1)


def solve_dlog_naive(g, h, dlog_max):
    """
    Naively attempts to solve for the discrete log x, where g^x = h, via trial and
    error. Assumes that x is at most dlog_max.
    """
    for j in range(dlog_max):
        if g ** j == h:
            return j
    return 0


def bsgs(g, h, p):
    '''
    Solve for x in h = g^x mod p given a prime p.
    If p is not prime, you shouldn't use BSGS anyway.
    '''
    N = math.ceil(math.sqrt(p - 1))  # phi(p) is p-1 if p is prime

    # Store hashmap of g^{1...m} (mod p). Baby step.
    tbl = {pow(g, i, p): i for i in range(N)}

    # Precompute via Fermat's Little Theorem
    c = pow(g, N * (p - 2), p)

    # Search for an equivalence in the table. Giant step.
    for j in range(N):
        y = (h * pow(c, j, p)) % p
        if y in tbl:
            return j * N + tbl[y]

    # Solution not found
    return None
