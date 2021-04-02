import json
from sys import argv
from row_set_gen import generate_row_objs
from find_prev_state import solve



def save_results(results):
    with open('i_o/output.json','w') as json_f:
            json.dump(results,json_f)


with open('i_o/input.json') as f:
    INITIAL_GRID = json.load(f)

if len(argv) == 1:
    print("Input num iterations")
    quit()

num_iterations = int(argv[1])

input_grid = INITIAL_GRID 
for i in range(num_iterations):
    generate_row_objs(input_grid)
    input_grid = solve(input_grid)



print('Storing solution in i_o/output.json...')
save_results(input_grid)
