from rpq import *
from rpq_reformat import *

import config
import warnings


# (a/(a+/b)+/b)+
# (((a+/b)+/c)+/d)+
# a/((a+/b)/b+/(c/e)/d)+
def to_rpq(ls):
    translated = []
    to_pop = []

    # Check if any of the objects are already translated
    for j in range(len(ls)):
        if not isinstance(ls[j], str):
            translated.append(ls[j])
            to_pop.append(j)

    # Rewrite the translated objects with a char '?' for 'join.split' operation
    if len(to_pop) != 0:
        for each in to_pop:
            ls[each] = '?'

    # Separate the objects by concatenation
    new_translated = []
    els = ''.join(ls).split('/')
    for i in range(len(els)):
        if '?' in els[i]:
            # case of '?'
            if els[i] == '?':
                els[i] = translated.pop(0)

            # case of '?+'
            else:
                new_translated.append(translated.pop(0))

    # Check if translated list is not empty
    if len(translated) != 0:
        warnings.warn("Warning: translated list is not empty!")

    # Translate each object and throw it into tr_ls list
    tr_ls = []
    for i in range(len(els)):
        # If translated throw into the list
        if not isinstance(els[i], str):
            tr_ls.append(els[i])
            continue

        # Plus RPQ cases
        if els[i][-1] == '+':
            # Case when we have a translated part with plus: ?+
            if '?' in els[i]:
                tr_ls.append(RPQ_Plus(new_translated.pop(0)))
            # Case when we have a Plus RPQ: a+
            else:
                tr_ls.append(RPQ_Plus(RPQ_Predicate(els[i][:-1])))
        # Case when we have just a Predicate: a
        else:
            tr_ls.append(RPQ_Predicate(els[i]))

    # Concatenate the objects of the tr_ls list
    final = tr_ls[0]
    for i in range(1, len(tr_ls)):
        final = RPQ_Concat(final, tr_ls[i])

    return final


def translate_file(file_rpq):
    stack = []
    current_list = []
    for each_char in file_rpq:
        # Save everything before each opening parenthesis
        if each_char == "(":
            stack.append(current_list)
            current_list = []

        # Translate the part in the parenthesis
        elif each_char == ")":
            current_list = to_rpq(current_list)
            previous_list = stack.pop()
            previous_list.append(current_list)
            current_list = previous_list
        else:
            current_list.append(each_char)

    current_list = to_rpq(current_list)
    return current_list


f = open('rpq.txt', "r")
read_rpq = f.read()

rpq_test = translate_file(read_rpq)

# final_cte = rpq_test.sql_translation()
# print(config.sql_full[:-2])
#
# print(f"SELECT x,y FROM {final_cte}")

new_rpq = rpq_reformat(rpq_test)

final_cte = new_rpq.sql_translation()
print(config.sql_full[:-2])
print(f"SELECT x,y FROM {final_cte}")
