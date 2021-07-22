import numpy as np
from charm.toolbox.pairinggroup import pair


def dot_product(CT1, CT2):
    ga, gp1, gp2 = CT1
    gb, gq1, gq2 = CT2

    ab_pair = pair(gq, gb)

    Eq1 = 1
    for i in range(len(gp1)):
        Eq1 *= pair(gp1[i], gq1[i])

    Eq2 = 1
    for i in range(len(gp2)):
        Eq2 *= pair(gp2[i], gq2[i])

    inner_product_pair = Eq1 * Eq2
