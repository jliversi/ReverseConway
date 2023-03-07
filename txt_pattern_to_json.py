import json
from sys import argv

if len(argv) == 1:
    print("No pattern provided")
    quit()

abc_folder = 'pattern_parsing/alphabet'

input_pattern = [
    '0000000'
]

for char in argv[1]:
    pattern_file = f'{abc_folder}/{char}.txt'
    with open(pattern_file) as f:
        input_pattern += [line.replace('\n','') for line in f.readlines()[1:]]

arr = []

for l in input_pattern:
    l_arr = []
    for char in l:
        l_arr.append(int(char))
    arr.append(l_arr)


output_path = f'pattern_parsing/output_patterns/{argv[1]}.json'
open(output_path,'x')

with open(output_path,'w') as json_f:
    json.dump(arr,json_f)

with open('i_o/input.json','w') as json_f:
    json.dump(arr,json_f)
