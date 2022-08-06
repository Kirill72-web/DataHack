import subprocess
import time
import os
import pandas as pd
import numpy as np
import json


flag1 = True
start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example',  '-r', '10000'], capture_output=True)
delta = time.time() - start

if process.stderr:
    print('Test 1: Failed:\n', process.stderr)
    flag1 = False

elif ' '.join(os.listdir()).find('example.csv') == -1 and flag1:
    print('Test 1: Failed:\n', 'file not generated')
    flag1 = False

if flag1:
    print('Test 1: Done, time:', delta)



