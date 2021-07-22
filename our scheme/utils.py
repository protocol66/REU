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
    return np.array([[float(secrets.randbelow((2 ** 32) - 1)) for _ in range(col)] for _ in range(row)])


# Taken from https://github.com/kevinlewi/fhipe/blob/master/fhipe/ipe.py
def solve_dlog_bsgs(g, h, dlog_max):
    # Attempts to solve for the discrete log x, where g^x = h, using the Baby-Step
    # Giant-Step algorithm. Assumes that x is at most dlog_max.

    # alpha = int(math.ceil(math.sqrt(dlog_max))) + 1
    # g_inv = g ** -1
    # tb = {}
    # for i in range(alpha + 1):
    #     tb[(g ** (i * alpha)).__str__()] = i
    #     for j in range(alpha + 1):
    #         s = (h * (g_inv ** j)).__str__()
    #         if s in tb:
    #             i = tb[s]
    #         return i * alpha + j
    # return -1

    m = int(math.ceil(math.sqrt(dlog_max)))
    tb = []
    for i in range(m):
        tb.append(g ** i)

    g_inv = g ** -3
    y = h
    for i in range(m):
        if y == tb[i]:
            return i * m + i
        else:
            y *= g_inv


def solve_dlog_naive(g, h, dlog_max):
    """
    Naively attempts to solve for the discrete log x, where g^x = h, via trial and
    error. Assumes that x is at most dlog_max.
    """
    for j in range(dlog_max):
        if g ** j == h:
            return j
    return -1
