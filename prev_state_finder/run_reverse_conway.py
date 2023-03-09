from datetime import datetime

from row_set_gen import generate_row_objs
from find_prev_state import find_prev_state
from util import print_now, time_since, print_grid, print_solution
from conway_io import save_results

SOLUTION = [[],0]
def run_back(grid, row_dict, label, max_depth=10, depth=0):
    if depth > SOLUTION[1]:
        print(f'{print_now()} - Solution of depth {depth} found') # TODO: move to printing functions in util
        save_results(grid, depth, label)
        SOLUTION[0] = grid
        SOLUTION[1] = depth
    
    if depth == max_depth:
        print(f'{print_now()} - Reached max search depth ({max_depth})') # TODO: move to printing functions in util
        return "Max search depth reached"

    generate_row_objs(grid, row_dict)
    for poss_solution in find_prev_state(grid, row_dict):
        result = run_back(poss_solution, row_dict, label, max_depth, depth + 1)
        if result:
            return "Max search depth reached"


def find_prev_to_depth(input_grid, row_dict, max_depth, label):
    row_length = len(input_grid[0])
    start_time = datetime.now()
    print(f'{print_now()} - Begin search for') # TODO: move these to some "re-solve print" function
    print_grid(input_grid) # TODO: move these to some "re-solve print" function
    print('') # TODO: move these to some "re-solve print" function

    result = run_back(input_grid, row_dict, label, max_depth)
    final_message = result or "Search exhausted"
    print(f'{print_now()} - {final_message}')

    if SOLUTION[1]:
        print(f'\nDeepest solution found {SOLUTION[1]} steps back')
        print_solution(SOLUTION[0],input_grid,SOLUTION[1])
        print(f'Solution saved in json/output/{SOLUTION[1]}.json')
    else:
        print('\nNo solution found for')
        print_grid(input_grid)

    print('')
    print(f'Total time, {time_since(start_time)} sec')
    return SOLUTION[0] if SOLUTION[1] else None



