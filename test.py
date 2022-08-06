import subprocess
import time
import os
import pandas as pd
import numpy as np


start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example', '-j', 'commands.json', '-r', '10000'], capture_output=True)
delta = time.time() - start

if process.stderr:
    print('Test 1: Failed:\n', process.stderr)
    exit()
elif ' '.join(os.listdir()).find('example.csv') == -1:
    print('Test 1: Failed:\n', 'file not generated')
    exit()
print('Test 1: Done, time:', delta)


