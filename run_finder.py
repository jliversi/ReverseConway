import json
import os
from datetime import datetime
from sys import argv
from row_set_gen import generate_row_objs
from find_prev_state import solutions



def save_results(results, input_string, depth):
    print(f'{print_now()} - Storing depth-{depth} solution in output/{input_string}/{depth}.json...')
    with open(f'output/{input_string}/{depth}.json','w') as json_f:
        json.dump(results,json_f)


SOLUTION = [[],0]
def run_back(grid, row_dict, input_string, max_depth=10, depth=0):
    if depth > SOLUTION[1]:
        print(f'{print_now()} - Solution of depth {depth} found')
        save_results(grid, input_string, depth)
        SOLUTION[0] = grid
        SOLUTION[1] = depth
    
    if depth == max_depth:
        print(f'{print_now()} - Reached max search depth ({max_depth})')
        return "Max search depth reached"

    generate_row_objs(grid, row_dict)
    for poss_solution in solutions(grid, row_dict):
        result = run_back(poss_solution, row_dict, input_string, max_depth, depth + 1)
        if result:
            return "Max search depth reached"


def solve(input_grid, row_dict, input_string, max_depth):
    row_length = len(input_grid[0])
    start_time = datetime.now()
    print(f'{print_now()} - Begin search for')
    print_grid(input_grid)
    print('')

    result = run_back(input_grid, row_dict, input_string, max_depth)
    final_message = result or "Search exhausted"
    print(f'{print_now()} - {final_message}')

    if SOLUTION[1]:
        print(f'\nDeepest solution found {SOLUTION[1]} steps back')
        print_solution(SOLUTION[0],input_grid,SOLUTION[1])
        print(f'Solution saved in output/{input_string}/{SOLUTION[1]}.json')
    else:
        print('\nNo solution found for')
        print_grid(input_grid)

    print('')
    print(f'Total time, {time_since(start_time)} sec')
    return SOLUTION[0] if SOLUTION[1] else None


def print_time(time):
    return time.strftime("%H:%M:%S")

def print_now():
    return print_time(datetime.now())

def time_since(time):
    return (datetime.now() - time).seconds

def print_solution(solution, original, depth):
    solution_flipped = reversed(list(zip(*solution)))
    original_flipped = reversed(list(zip(*original)))
    mid_point = len(solution[0])//2
    i = 0
    for l1, l2  in zip(solution_flipped, original_flipped):
        seperator = f' --({depth})--> ' if i == mid_point else '          '
        if depth > 9 and i != mid_point:
            seperator += ' '
        left = ''.join(['.' if x == 0 else '#' for x in l1])
        right = ''.join(['.' if x == 0 else '#' for x in l2])
        print(left + seperator + right)
        i += 1

def print_grid(grid):
    grid_flipped = reversed(list(zip(*grid)))
    for line in grid_flipped:
        print(''.join(['.' if x == 0 else '#' for x in line]))


def input_string_to_json(input_string):
    filename = f'pattern_parsing/json_patterns/{input_string}.json'
    if os.path.isfile(filename):
        with open(filename) as f:
            return json.load(f)

    abc_folder = 'pattern_parsing/alphabet'
    input_pattern = ['00000']
    for char in input_string:
        pattern_file = f'{abc_folder}/{char}.txt'
        with open(pattern_file) as f:
            input_pattern += [line.replace('\n','') for line in f]
            input_pattern.append('00000')

    arr = []
    for l in input_pattern:
        l_arr = []
        for char in l:
            l_arr.append(int(char))
        arr.append(l_arr)

    open(filename,'x')
    with open(filename,'w') as json_f:
        json.dump(arr,json_f)
    return arr



if __name__ == "__main__":
    if len(argv) == 1:
        print("No pattern provided")
        quit()

    INPUT_STRING = argv[1]
    MAX_DEPTH = 10
    if len(argv) == 3:
        MAX_DEPTH = int(argv[2])

    dir_name = f'{os.getcwd()}/output/{INPUT_STRING}'
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)
    ROW_DICT = dict()
    INITIAL_GRID = input_string_to_json(INPUT_STRING)
    result = solve(INITIAL_GRID, ROW_DICT, INPUT_STRING, MAX_DEPTH)









