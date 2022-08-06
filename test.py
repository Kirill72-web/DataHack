import subprocess
import time
import os

start = time.time()
process = subprocess.run(['python', 'generator.py', '-f', 'example', '-j', 'commands.json', '-r', '10000'], capture_output=True)
delta = time.time() - start
if ' '.join(os.listdir()).find('example.csv') != -1:
    print('Test 1: Done, time:', delta)
else:
    print('Test 1: Failed:\n', process.stderr if process.stderr else 'file not generated')



