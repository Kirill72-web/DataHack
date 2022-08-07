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
        return pd.Series(sorted(col.unique())).compare(pd.Series(sorted(un))).empty
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
print('all data types with out json')
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

if len(table[table.columns[0]]) == 10000:
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
print('not all data types with out json')
flag1 = True
start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example2', '-r', '10000'], capture_output=True)
delta = time.time() - start

if process.stderr:
    print('Test 1: Failed:\n', process.stderr)
    flag1 = False
    exit()
elif ' '.join(os.listdir()).find('example2.parquet') == -1 and flag1:
    print('Test 1: Failed:\n', 'file not generated')
    flag1 = False
    exit()

if flag1:
    print('Test 1: Done, time:', delta)

info = process.stdout.decode('utf-8').split('\r\n')
del info[0], info[-1], info[-1]
info = np.asarray(list(map(getInfo, info)))
table = pd.read_parquet('example2.parquet')

if len(table.columns) == len(info[:, 0]):
    print("Test 2: Done")
else:
    print("Test 2: Failed: not all columns")

if len(table[table.columns[0]]) == 10000:
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
print('all data types overridden in json')
flag1 = True
start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example', '-r', '10000', '-j', 'commands.json'], capture_output=True)
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

if len(table[table.columns[0]]) == 10000:
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
print('not all data types overridden in json')
flag1 = True
start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example', '-r', '10000', '-j', 'commands2.json'], capture_output=True)
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

if len(table[table.columns[0]]) == 10000:
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

print('join key test')
flag1 = True
start = time.time()
process1 = subprocess.run(['python', 'generator.py', '-f', 'example_join', '-r', '10000'], capture_output=True)
process2 = subprocess.run(['python', 'generator.py', '-f', 'example_join_s', '-r', '10000'], capture_output=True)
delta = time.time() - start

if process1.stderr or process2.stderr :
    print('Test 1: Failed:\n', process.stderr if process1.stderr else process2.stderr )
    flag1 = False
    exit()
elif ' '.join(os.listdir()).find('example_join.parquet') == -1 and ' '.join(os.listdir()).find('example_join_s.parquet') == -1 and flag1:
    print('Test 1: Failed:\n', 'file not generated')
    flag1 = False
    exit()

if flag1:
    print('Test 1: Done, time:', delta)

info1 = process1.stdout.decode('utf-8').split('\r\n')
del info1[0], info1[-1], info1[-1]
info1 = np.asarray(list(map(getInfo, info1)))
table = pd.read_parquet('example_join.parquet')
info2 = process2.stdout.decode('utf-8').split('\r\n')
del info2[0], info2[-1], info2[-1]
info2 = np.asarray(list(map(getInfo, info2)))
table2 = pd.read_parquet('example_join.parquet')
if len(table.columns) == len(info1[:, 0]) and len(table2.columns) == len(info2[:, 0]):
    print("Test 2: Done")
else:
    print("Test 2: Failed: not all columns")

if len(table[table.columns[0]]) == 10000 and len(table2[table2.columns[0]]) == 10000:
    print("Test 3: Done")
else:
    print("Test 3: Failed: not all rows")

for ind, i in enumerate(info1[:, 1]):
    if i == 'SetChoice':
        if choiceTest(table[info1[ind][0]], info1[ind][2].replace('[', '').replace(']', '').split(',')):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Date':
        if dateTest(table[info1[ind][0]], info1[ind][2].split(',')[0], info1[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Float':
        if floatTest(table[info1[ind][0]], float(info1[ind][2].split(',')[0]), float(info1[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Integer':
        if intTest(table[info1[ind][0]], int(info1[ind][2].split(',')[0]), int(info1[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Mask':
        if maskTest(table[info1[ind][0]], info1[ind][2].replace('[', '').replace(']', '').split(',')[0]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'String':

        if stringTest(table[info1[ind][0]], info1[ind][2].replace('[', '').split(']')[0].split(',')[:-1], info1[ind][2].replace('[', '').split(']')[0].split(',')[-1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'TimeStep':
        if tsTest(table[info1[ind][0]], info1[ind][2].split(',')[0], info1[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'WeighedChoice':
        if wchoiceTest(table[info1[ind][0]], info1[ind][2].split(' ')[0].split(','), info1[ind][2].split(' ')[1].split(','), 10000):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
for ind, i in enumerate(info2[:, 1]):
    if i == 'SetChoice':
        if choiceTest(table2[info2[ind][0]], info2[ind][2].replace('[', '').replace(']', '').split(',')):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Date':
        if dateTest(table2[info2[ind][0]], info2[ind][2].split(',')[0], info2[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Float':
        if floatTest(table2[info2[ind][0]], float(info2[ind][2].split(',')[0]), float(info2[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Integer':
        if intTest(table2[info2[ind][0]], int(info2[ind][2].split(',')[0]), int(info2[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Mask':
        if maskTest(table2[info2[ind][0]], info2[ind][2].replace('[', '').replace(']', '').split(',')[0]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'String':

        if stringTest(table2[info2[ind][0]], info2[ind][2].replace('[', '').split(']')[0].split(',')[:-1], info2[ind][2].replace('[', '').split(']')[0].split(',')[-1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'TimeStep':
        if tsTest(table2[info2[ind][0]], info2[ind][2].split(',')[0], info2[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'WeighedChoice':
        if wchoiceTest(table2[info2[ind][0]], info2[ind][2].split(' ')[0].split(','), info2[ind][2].split(' ')[1].split(','), 10000):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
key = np.asarray([[name, arg_] for name, type_, arg_ in info2 if type_ == "Alias" ])
flag2 = True
try:
    for i in key:
        if table[i[1]].compare(table2[i[0]]).empty:
            print(f"Test of {i[0]} Done")
            flag2 = False
    if flag2:
        print('Test of key Failed')
except:
    print('Test of key Failed')
print('join key test by 3')
flag1 = True
start = time.time()
process1 = subprocess.run(['python', 'generator.py', '-f', 'example_join_by_3_col', '-r', '10000'], capture_output=True)
process2 = subprocess.run(['python', 'generator.py', '-f', 'example_join_by_3_col_s', '-r', '10000'], capture_output=True)
delta = time.time() - start

if process1.stderr or process2.stderr :
    print('Test 1: Failed:\n', process.stderr if process1.stderr else process2.stderr )
    flag1 = False
    exit()
elif ' '.join(os.listdir()).find('example_join_by_3_col_s.parquet') == -1 and ' '.join(os.listdir()).find('example_join_by_3_col.parquet') == -1 and flag1:
    print('Test 1: Failed:\n', 'file not generated')
    flag1 = False
    exit()

if flag1:
    print('Test 1: Done, time:', delta)

info1 = process1.stdout.decode('utf-8').split('\r\n')
del info1[0], info1[-1], info1[-1]
info1 = np.asarray(list(map(getInfo, info1)))
table = pd.read_parquet('example_join_by_3_col.parquet')
info2 = process2.stdout.decode('utf-8').split('\r\n')
del info2[0], info2[-1], info2[-1]
info2 = np.asarray(list(map(getInfo, info2)))
table2 = pd.read_parquet('example_join_by_3_col_s.parquet')
if len(table.columns) == len(info1[:, 0]) and len(table2.columns) == len(info2[:, 0]):
    print("Test 2: Done")
else:
    print("Test 2: Failed: not all columns")

if len(table[table.columns[0]]) == 10000 and len(table2[table2.columns[0]]) == 10000:
    print("Test 3: Done")
else:
    print("Test 3: Failed: not all rows")

for ind, i in enumerate(info1[:, 1]):
    if i == 'SetChoice':
        if choiceTest(table[info1[ind][0]], info1[ind][2].replace('[', '').replace(']', '').split(',')):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Date':
        if dateTest(table[info1[ind][0]], info1[ind][2].split(',')[0], info1[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Float':
        if floatTest(table[info1[ind][0]], float(info1[ind][2].split(',')[0]), float(info1[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Integer':
        if intTest(table[info1[ind][0]], int(info1[ind][2].split(',')[0]), int(info1[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Mask':
        if maskTest(table[info1[ind][0]], info1[ind][2].replace('[', '').replace(']', '').split(',')[0]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'String':

        if stringTest(table[info1[ind][0]], info1[ind][2].replace('[', '').split(']')[0].split(',')[:-1], info1[ind][2].replace('[', '').split(']')[0].split(',')[-1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'TimeStep':
        if tsTest(table[info1[ind][0]], info1[ind][2].split(',')[0], info1[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'WeighedChoice':
        if wchoiceTest(table[info1[ind][0]], info1[ind][2].split(' ')[0].split(','), info1[ind][2].split(' ')[1].split(','), 10000):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")

for ind, i in enumerate(info2[:, 1]):
    if i == 'SetChoice':
        if choiceTest(table2[info2[ind][0]], info2[ind][2].replace('[', '').replace(']', '').split(',')):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Date':
        if dateTest(table2[info2[ind][0]], info2[ind][2].split(',')[0], info2[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Float':
        if floatTest(table2[info2[ind][0]], float(info2[ind][2].split(',')[0]), float(info2[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Integer':
        if intTest(table2[info2[ind][0]], int(info2[ind][2].split(',')[0]), int(info2[ind][2].split(',')[1])):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'Mask':
        if maskTest(table2[info2[ind][0]], info2[ind][2].replace('[', '').replace(']', '').split(',')[0]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'String':

        if stringTest(table2[info2[ind][0]], info2[ind][2].replace('[', '').split(']')[0].split(',')[:-1], info2[ind][2].replace('[', '').split(']')[0].split(',')[-1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'TimeStep':
        if tsTest(table2[info2[ind][0]], info2[ind][2].split(',')[0], info2[ind][2].split(',')[1]):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")
    elif i == 'WeighedChoice':
        if wchoiceTest(table2[info2[ind][0]], info2[ind][2].split(' ')[0].split(','), info2[ind][2].split(' ')[1].split(','), 10000):
            print(f"Test of {i} Done")
        else:
            print(f"Test of {i} Failed")

key = np.asarray([[name, arg_] for name, type_, arg_ in info2 if type_ == "Alias" ])


flag2 = True
try:
    for i in key:
        if table[i[1]].compare(table2[i[0]]).empty:
            print(f"Test of {i[0]} Done")
            flag2 = False
    if flag2:
        print('Test of keys by 3 cols Failed')
except:
    print('Test of keys by 3 cols Failed')
