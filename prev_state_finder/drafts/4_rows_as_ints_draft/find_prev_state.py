import pickle
import json
from datetime import datetime
# Now that we can find all possible patterns for any given row,
# we can take multiple rows and then just need to find a path through their possiblities

# Here we go!
# After passing each row into through `poss_row_patterns`, collect results in list
# pass that list to solve, will recursively search for mergable path through that list
# returns a list of three-row-integer-tuples
# TODO: REFACTOR TO WORK WITH THE POSSES ALREADY SORTED INTO TOPS AND BOTTOMS
# ^^^^ THIS MEANS NO NEED FOR MERGE CHECK FILTER
# TODO: Sorta did ^^, so annotate accordingly
def find_grid_pattern(row_len,poss_per_row_list, current_posses=None, depth=0):
    # if on first level, options aren't filtered yet, so just grab options for top row
    if depth == 0:
        a = poss_per_row_list[0]
        current_posses = [poss for poss_key in a for poss in a[poss_key]]

    # if reached bottom level (!!!), let's hope possiblities are non-empty...
    # if so, just return first option
    if depth == len(poss_per_row_list) - 1:
        for el in current_posses:
            return [el]

    # iterate current options
    for top_trio in current_posses:
        # filter next set of possibilites
        bottom_two_of_trio = top_trio & (2**(row_len * 2) - 1)
        if bottom_two_of_trio not in poss_per_row_list[depth + 1]: continue
        poss_next = poss_per_row_list[depth + 1][bottom_two_of_trio]
        
        # recurse with those possibilties
        subresult = find_grid_pattern(row_len,poss_per_row_list, poss_next, depth + 1)
        # if subresult is truthy, we found it! send it up!!!!
        if subresult:
            return [top_trio] + subresult
        # otherwise continue to next iteration of current_posses

    # if never found, return None for recursive results
    return None

# The hard work done, parse the result of `find_grid_pattern` into
# a 2D array of 1s and 0s, ready for JSONificiation
def format_results(grid_pattern, row_length):
    # TODO: REMOVE (FOR TESTING)
    for el in grid_pattern:
        rows_int_to_display(el, row_length)
        print()

    first = grid_pattern[0]
    # convert first row-integer into binary string for first 2 rows
    first_2_rows = format((first >> row_length), f'0{row_length * 2}b')
    # then turn them into arrays of 1s and 0s and begin result
    row1 = [int(char) for char in first_2_rows[:row_length]]
    row2 = [int(char) for char in first_2_rows[row_length:]]
    result = [row1, row2]
    # add rest of rows in grid_pattern
    for row_trio in grid_pattern:
        # for these we only care about the final {row_length} digits
        third_row = row_trio & (2**row_length - 1)
        row_str = format(third_row, f'0{row_length}b')
        result.append([int(char) for char in row_str])

    return result


# bring it all together, takes a 2D array (N x N) of desired pattern
# returns 2D array (N+2 x N+2) of prev state
def solve(input_grid):
    row_length = len(input_grid[0])
    start_time = datetime.now()
    print(f'Started at {start_time.strftime("%H:%M:%S")}')
    all_poss_row_patterns = []
    print(f'Fetching partial solutions per row...')
    fetched = {}
    for row in input_grid:
        row_name = ''.join([str(x) for x in row])
        if row_name in fetched:
            all_poss_row_patterns.append(fetched[row_name])
        else:
            file_name = f'obj_files/{row_name}.obj'
            with open(file_name,'rb') as row_file:
                row_posses = pickle.load(row_file) 
                fetched[row_name] = row_posses
                all_poss_row_patterns.append(row_posses)

    now = (datetime.now() - start_time).seconds
    print(len(all_poss_row_patterns),f'rows fetched after {now} secs')
    print('Searching for full solution...')
    found_pattern = find_grid_pattern(row_length + 2, all_poss_row_patterns)
    now = (datetime.now() - start_time).seconds
    print(f'Solution found after {now} secs')
    print('Formatting results...')
    formatted = format_results(found_pattern, row_length + 2)
    with open('i_o/output.json','w') as json_f:
        json.dump(formatted,json_f)
    print('\nSolution: (stored in i_o/output.json)')
    for el in formatted:
        print(''.join(['.' if x == 0 else '#' for x in el]))
    print('\n')

    end_time = datetime.now()
    runtime_in_seconds = (end_time - start_time).seconds
    print(f'Finished at {end_time.strftime("%H:%M:%S")}')
    print(f'Total time, {runtime_in_seconds} sec')




# MAKE IT HAPPEN

with open('i_o/input.json') as f:
    input_grid = json.load(f)


# solve(input_grid)



# for testing
def num_to_3x3_display(num):
    print(num)
    num = format(num, '09b')
    print(num)
    print(num[0],num[3],num[6])
    print(num[1],num[4],num[7])
    print(num[2],num[5],num[8])

def rows_int_to_display(num, row_len):
    print(num)
    num = format(num, f'0{row_len * 3}b')
    print(num)
    rows = ['','','']
    for i in range(row_len * 3):
        row_idx = i // row_len
        rows[row_idx] += num[i]
    for el in rows:
        print(el)

solve(input_grid)









# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!
# LEGACY HERE!!!




# The hard work done, parse the result of `find_grid_pattern` into
# # a 2D array of 1s and 0s (nice and human readable)
# # TODO: ENTIRELY RE-WRITE THIS TO WORK WITH NEW row_len*3 length ints 
# def format_results1(grid_pattern, row_length):
#     result = []
#     first = grid_pattern[0]
#     # convert each row-integer into binary string
#     row1_string = format(first[0], f'0{row_length}b')
#     # then map each character to integer (1 or 0)
#     # and reverse (undoing reverse from `sqr_ints_to_row_ints`)
#     result.append(list(reversed(list(map(int, row1_string)))))

#     row2_string = format(first[1], f'0{row_length}b')
#     result.append(list(reversed(list(map(int, row2_string)))))

#     # repeat for third row of all first and all other rows-tuples
#     for row in grid_pattern:
#         row_string = format(row[2], f'0{row_length}b')
#         result.append(list(reversed(list(map(int, row_string)))))

#     return result