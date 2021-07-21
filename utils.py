import socket
import pickle
import numpy as np
from charm.toolbox.pairinggroup import ZR


# node is a tuple (h, o)
def RepNodes(node, a):
    # print(node)
    # print(a)
    if node[0] <= 0:
        return []

    leftNode = (node[0] - 1, 2 * node[1])
    rightNode = (node[0] - 1, 2 * node[1] + 1)

    if ((rightNode[1] + 1) * (2 ** rightNode[0])) < a:
        print(f'larger than {((rightNode[1] + 1) * (2 ** rightNode[0]))}')

    if (node[1] + 1) * (2 ** node[0]) - 1 == a:
        return [node]

    if (rightNode[1] * (2 ** rightNode[0])) <= a < ((rightNode[1] + 1) * (2 ** rightNode[0])):
        return [leftNode] + RepNodes(rightNode, a)

    return RepNodes(leftNode, a)


def CoveringNodes(node, root):
    if node[0] == root[0]:
        return [root]
    elif node[1] % 2 == 0:
        parent = (node[0] + 1, node[1] // 2)
    else:
        parent = (node[0] + 1, (node[1] - 1) // 2)

    return [node] + CoveringNodes(parent, root)


def splitBits(value, n):
    ''' Split `value` into a list of `n`-bit integers '''
    value = int(value)
    original = value
    mask = (1 << n) - 1
    segments = []
    if value == 0:
        segments.append(0)
    while value and (original.bit_length() / n) > len(segments):
        segments.append(value & mask)
        value >>= n
    segments.reverse()
    return segments


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
    return np.array([[float(int(group.random(ZR))) for _ in range(col)] for _ in range(row)])
