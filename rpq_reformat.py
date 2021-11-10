"""
    File name: rpq_reformat.py
    Author: Temur Malishava
"""
from rpq import *


# ((a+/b)+/c+)+ => ((a*/(a/b))*/((a*/(a/b))/c))+
def rpq_reformat(rpq):
    if isinstance(rpq, RPQ_Plus):
        rpq = RPQ_Plus(rpq_reformat(rpq.subRPQ))

    if isinstance(rpq, RPQ_Concat):
        l = rpq_reformat(rpq.left_subRPQ)  # a+
        r = rpq_reformat(rpq.right_subRPQ)  # b
        rpq = inner_reform(l, r)

    return rpq


def inner_reform(left, right):
    main = None

    if isinstance(left, RPQ_Plus) and isinstance(right, RPQ_Plus):  # a+/b+
        main = RPQ_S(left.subRPQ, RPQ_Concat(left.subRPQ, right.subRPQ), right.subRPQ)  # a, (a/b), b

    if isinstance(left, RPQ_Plus) and not isinstance(right, RPQ_Plus):  # a+/b
        main = RPQ_S(left.subRPQ, RPQ_Concat(left.subRPQ, right), None)  # a, (a/b), None

    if not isinstance(left, RPQ_Plus) and isinstance(right, RPQ_Plus):  # a/b+
        main = RPQ_S(None, RPQ_Concat(left, right.subRPQ), right.subRPQ)  # None, (a/b), b

    if main is not None:
        return main

    # a/b
    else:
        return RPQ_Concat(left, right)

