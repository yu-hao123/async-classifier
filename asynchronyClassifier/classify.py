'''
Detect and classify asynchronies

all of the methods below expects ins_marks and exp_marks arrays with the same size
the same goes with pmus_start_marks and pmus_finish_marks
also ins_marks[0] < exp_marks[0] and pmus_start_marks[0] < pmus_finish_marks[0]

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
                  exp_marks[j] > pmus_start_marks[i]
                  ):
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


def find_reverse_trigger(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks):
    single_indexes = []
    double_indexes = []

    for i in range(len(pmus_start_marks)):
        for j in range(len(ins_marks)):
            if (j >= len(exp_marks) and ins_marks[j] < pmus_start_marks[i]):
                single_indexes.append(ins_marks[j])
                break
            if (ins_marks[j] < pmus_start_marks[i] and exp_marks[j] > pmus_start_marks[i]):
                if (j + 1 >= len(exp_marks) or j + 1 >= len(ins_marks)):
                    single_indexes.append(ins_marks[j])
                    break
                elif (ins_marks[j + 1] < pmus_finish_marks[i]):
                    double_indexes.append(ins_marks[j])
                else:
                    single_indexes.append(ins_marks[j])
    return single_indexes, double_indexes


def find_double_trigger(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks):
    indexes = []
    for i in range(len(pmus_start_marks)):
        for j in range(1, len(ins_marks) - 1):
            if (ins_marks[j] > pmus_start_marks[i] and ins_marks[j] < pmus_finish_marks[i]):
                if (exp_marks[j - 1] < pmus_start_marks[i] and ins_marks[j + 1] < pmus_finish_marks[i]):
                    indexes.append(pmus_start_marks[i])
    return indexes


def find_late_cycling(ins_marks, exp_marks, pmus_start_marks, pmus_finish_marks):
    indexes = []
    for i in range(len(pmus_start_marks) - 1):
        for j in range(len(exp_marks)):
            if(exp_marks[j] >= pmus_finish_marks[i] and exp_marks[j] <= pmus_start_marks[i + 1]):
                if (ins_marks[j] <= pmus_finish_marks[i] and ins_marks[j] >= pmus_start_marks[i]):
                    indexes.append(pmus_start_marks[i])
    return indexes

def find_early_cycling(ins_marks, exp_marks, pmus_start_marks, pmus_peak_marks):
    indexes = []
    for i in range(len(pmus_start_marks)):
        for j in range(len(exp_marks)):
            if (exp_marks[j] <= pmus_peak_marks[i] and exp_marks[j] >= pmus_start_marks[i]):
                if (ins_marks[j] <= pmus_peak_marks[i] and ins_marks[j] >= pmus_start_marks[i]):
                    indexes.append(pmus_start_marks[i])
    return indexes