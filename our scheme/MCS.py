import socket
from charm.toolbox.pairinggroup import pair, PairingGroup
from utils import send, recv, solve_dlog_bsgs, solve_dlog_naive, bsgs


def decision_function(CT1, CT2, dlog_max, group):
    ga, gp1, gp2 = CT1
    gb, gq1, gq2 = CT2

    # assert ga.initPP(), "ERROR: Failed to init pre-computation table for g1."
    # assert gb.initPP(), "ERROR: Failed to init pre-computation table for g2."

    ab_pair = group.pair_prod(ga, gb)

    Eq1 = 1
    for i in range(len(gp1)):
        Eq1 *= group.pair_prod(gp1[i], gq1[i])

    Eq2 = 1
    for i in range(len(gp2)):
        Eq2 *= group.pair_prod(gp2[i], gq2[i])

    inner_product_pair = Eq1 * Eq2
    
    # decision_func = ab_pair * inner_product_pair

    # return solve_dlog_naive(ab_pair, inner_product_pair, dlog_max)
    return solve_dlog_bsgs(ab_pair, inner_product_pair, dlog_max)
    # return bsgs(ab_pair, inner_product_pair, dlog_max)

# DO_PORT = 2000
# MCS_PORT = 2001
# DU_PORT = 2002
#
#
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#
# s.bind((socket.gethostname(), MCS_PORT))
# s.listen(5)
#
# print("receiving group")
# group_name = recv(s)
# group = PairingGroup(group_name)
# print("receiving CT1")
# CT1_serialized = recv(s)
# print("sending signal")
# send(True, DU_PORT)
# print("receiving CT2")
# CT2_serialized = recv(s)
#
# CT1 = []
# for i in CT1_serialized:
#     ga, gp1, gp2 = i
#     gp1 = [group.deserialize(j) for j in gp1]
#     gp2 = [group.deserialize(j) for j in gp2]
#     CT1.append((group.deserialize(ga), gp1, gp2))
#
# gb, gq1, gq2 = CT2_serialized
# gq1 = [group.deserialize(j) for j in gq1]
# gq2 = [group.deserialize(j) for j in gq2]
# CT2 = (group.deserialize(gb), gq1, gq2)
#
# print("order", group.order())
# decision_functions = []
# for i in CT1:
#     decision_functions.append(decision_function(i, CT2, group.order(), group))
#
# print(decision_functions)

