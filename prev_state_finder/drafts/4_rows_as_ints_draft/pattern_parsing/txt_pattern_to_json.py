import json
from sys import argv
import os.path

if len(argv) == 1:
    print("No pattern filename provided")
    quit()

pattern_file = f'patterns/{argv[1]}'
with open(pattern_file) as f:
    input_pattern = [line.replace('\n','') for line in f]

arr = []

for l in input_pattern:
    l_arr = []
    for char in l:
        l_arr.append(int(char))
    arr.append(l_arr)



dirname = os.path.dirname(os.path.dirname(__file__))
output_file = os.path.join(dirname, 'i_o/input.json')
    
with open(output_file,'w') as json_f:
    json.dump(arr,json_f)