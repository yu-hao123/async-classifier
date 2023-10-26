'''
Detect and classify asynchronies

'''

import numpy as np

def find_ineffective_effort(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks):
    indexes = []
    for i in range(len(pmus_start_marks)):
        detected = True
        if (i >= len(pmus_finish_marks)):
            break
        for j in range(len(ins_marks)):
            if (ins_marks[j] > pmus_start_marks[i] and \
                ins_marks[j] < pmus_finish_marks[i]
                ):
                detected = False
            if (j < len(exp_marks) and \
                exp_marks[j] > pmus_start_marks[i] and \
                exp_marks[j] < pmus_finish_marks[i]
                ):
                detected = False

            # if pmus effort is in the inspiration part of the flow cycle
            # there is not IEE
            if (j >= len(exp_marks) and ins_marks[j] < pmus_start_marks[i]):
                detected = False
            elif (ins_marks[j] < pmus_start_marks[i] and \
                  exp_marks[j] > pmus_start_marks[i]):
                detected = False

        if (detected):
            indexes.append(pmus_start_marks[i])
    return indexes


def find_auto_trigger(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks):
    indexes = []
    for i in range(len(pmus_finish_marks)):
        if (i + 1 >= len(pmus_start_marks)):
            break
        next_ins = pmus_start_marks[i + 1]
        for j in range(len(ins_marks)):
            if (ins_marks[j] > pmus_finish_marks[i] and ins_marks[j] < next_ins):
                if (j >= len(exp_marks)):
                    break
                if (exp_marks[j] > pmus_finish_marks[i] and exp_marks[j] < next_ins):
                    indexes.append(ins_marks[j])
    return indexes