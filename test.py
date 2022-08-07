import json
import numpy as np
import os
import pandas as pd
import subprocess
import time
from sys import exit
import time

def getInfo(text):
    res = text.replace('(', '').replace(')', '').replace("'", '').replace("<class datahack.", '').replace(', ',
                                                                                                          ',').replace(
        '> ', ' ').replace(',[', ' ').replace('[', '').replace(']', '').split(' ')
    if len(res) > 3:
        res[2] = ' '.join(res[2:])
        del res[3:]
    return res


def choiceTest(col, un):
    if len(col.unique()) == len(un):
        return col.unique().tolist() in np.asarray(un)
    return False

def wchoiceTest(col, un, unw, rows):
    if len(col.value_counts()) == len(un) and len(un) == len(unw):
        col = col.value_counts() / rows * 100
        for i in range(len(un)):
            if col[i] < float(sorted(unw, reverse=True)[i]) -5 and col[i] > float(sorted(unw, reverse=True)[i]) + 5:
                return False
        return True
    return False

def floatTest(col, min, max):
    return ((col <= np.ones_like(col) * max) & (col >= np.ones_like(col) * min)).all()

def intTest(col, min, max):
    return ((col <= np.ones_like(col) * max) & (col >= np.ones_like(col) * min)).all()

def stringTest(col, symbols, maxLen=False):
    if maxLen:
        boolList = [el for el in col if len(el) != maxLen or len([x for x in el if x not in symbols]) != 0]
        if not boolList:
            return False
        return True
    else:
        boolList = [el for el in col if len(el) > 100 or len([x for x in el if x not in symbols]) != 0]
        if not boolLists:
            return False
        return True

def dateTest(col, start, stop):
    for el in col:
        try:
            t = time.strptime(el, '%Y-%m-%d')
            if t < time.strptime(start, '%Y-%m-%d') and time.strptime(stop, '%Y-%m-%d') < t:
                return False
        except:
            return False
    return True

def tsTest(col, start, stop):
    for el in col:
        try:
            t = time.strptime(el, '%Y-%m-%d %H:%M:%S')
            if t < time.strptime(start, '%Y-%m-%d %H:%M:%S') and time.strptime(stop, '%Y-%m-%d %H:%M:%S') < t:
                return False
        except:
            return False
    return True

def maskTest(col, mask):
    for i in col:
        if i.find('#') != -1 and len(mask) != len(i):
            return False
    return True

flag1 = True
start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example', '-r', '10000'], capture_output=True)
delta = time.time() - start

if process.stderr:
    print('Test 1: Failed:\n', process.stderr)
    flag1 = False
    exit()
elif ' '.join(os.listdir()).find('example.parquet') == -1 and flag1:
    print('Test 1: Failed:\n', 'file not generated')
    flag1 = False
    exit()

if flag1:
    print('Test 1: Done, time:', delta)

info = process.stdout.decode('utf-8').split('\r\n')
del info[0], info[-1], info[-1]
info = np.asarray(list(map(getInfo, info)))
table = pd.read_parquet('example.parquet')

if len(table.columns) == len(info[:, 0]):
    print("Test 2: Done")
else:
    print("Test 2: Failed: not all columns")

if len(table[table.columns]) == 10000:
    print("Test 3: Done")
else:
    print("Test 3: Failed: not all rows")


for ind, i in enumerate(info[:, 1]):
    if i == 'SetChoice':
        if choiceTest(table[info[ind][0]], info[ind][2].replace('[', '').replace(']', '').split(',')):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Date':
        if dateTest(table[info[ind][0]], info[ind][2].split(',')[0], info[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Float':
        if floatTest(table[info[ind][0]], float(info[ind][2].split(',')[0]), float(info[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Integer':
        if intTest(table[info[ind][0]], int(info[ind][2].split(',')[0]), int(info[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Mask':
        if maskTest(table[info[ind][0]], info[ind][2].replace('[', '').replace(']', '').split(',')[0]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'String':

        if stringTest(table[info[ind][0]], info[ind][2].replace('[', '').split(']')[0].split(',')[:-1], info[ind][2].replace('[', '').split(']')[0].split(',')[-1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'TimeStep':
        if tsTest(table[info[ind][0]], info[ind][2].split(',')[0], info[ind][2].split(',')[1] ):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'WeighedChoice':
        if wchoiceTest(table[info[ind][0]], info[ind][2].split(' ')[0].split(','), info[ind][2].split(' ')[1].split(','), 10000):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
