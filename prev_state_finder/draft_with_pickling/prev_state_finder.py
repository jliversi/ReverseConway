import pickle
# Now that we can find all possible patterns for any given row,
# we can take multiple rows and then just need to find a path through their possiblities

# Here we go!
# After passing each row into through `poss_row_patterns`, collect results in list
# pass that list to solve, will recursively search for mergable path through that list
# returns a list of three-row-integer-tuples
# TODO: REFACTOR TO WORK WITH THE POSSES ALREADY SORTED INTO TOPS AND BOTTOMS
# ^^^^ THIS MEANS NO NEED FOR MERGE CHECK FILTER
# TODO: Sorta did ^^, so annotate accordingly
def find_grid_pattern(poss_per_row_list, current_posses=None, depth=0):
    # if on first level, options aren't filtered yet, so just grab first set
    if depth == 0:
        a = poss_per_row_list[0]
        current_posses = [poss for poss_key in a for poss in a[poss_key]]

    # if reached bottom level (!!!), let's hope possiblities are non-empty...
    # if so, just return first option
    if depth == len(poss_per_row_list) - 1:
        for el in current_posses:
            return [el]

    # iterate current options
    for top in current_posses:
        # filter next set of possibilites
        if top[1:] not in poss_per_row_list[depth + 1]: continue
        poss_next = poss_per_row_list[depth + 1][top[1:]]
        
        # recurse with those possibilties
        subresult = find_grid_pattern(poss_per_row_list, poss_next, depth + 1)
        # if subresult is truthy, we found it! send it up!!!!
        if subresult:
            return [top] + subresult
        # otherwise continue to next iteration of current_posses

    # if never found, return None for recursive results
    return None


# The hard work done, parse the result of `find_grid_pattern` into
# a 2D array of 1s and 0s (nice and human readable)
def format_results(grid_pattern, row_length):
    result = []
    first = grid_pattern[0]
    # convert each row-integer into binary string
    row1_string = format(first[0], f'0{row_length}b')
    # then map each character to integer (1 or 0)
    # and reverse (undoing reverse from `sqr_ints_to_row_ints`)
    result.append(list(reversed(list(map(int, row1_string)))))

    row2_string = format(first[1], f'0{row_length}b')
    result.append(list(reversed(list(map(int, row2_string)))))

    # repeat for third row of all first and all other rows-tuples
    for row in grid_pattern:
        row_string = format(row[2], f'0{row_length}b')
        result.append(list(reversed(list(map(int, row_string)))))

    return result



# bring it all together, takes a 2D array (N x N) of desired pattern
# returns 2D array (N+2 x N+2) of prev state
def solve(all_poss_row_patterns, row_length):
    now = (datetime.now() - start_time).seconds
    print(f'{now} secs: Searching for full solution...')
    found_pattern = find_grid_pattern(all_poss_row_patterns)
    now = (datetime.now() - start_time).seconds
    print(f'{now} secs: Formatting results...')
    return format_results(found_pattern, row_length + 2)




# MAKE IT HAPPEN


from datetime import datetime



with open('pattern.txt') as f:
    INPUTS = [line.replace('\n','') for line in f]



start_time = datetime.now()
print(f'Started at {start_time.strftime("%H:%M:%S")}')
row_patterns = []
now = (datetime.now() - start_time).seconds
print(f'{now} secs: Fetching partial solutions per row...')
fetched = {}
for i, row in enumerate(INPUTS):
    if row in fetched:
        row_patterns.append(fetched[row])
    else:
        file_name = f'obj_files/{row}.obj'
        with open(file_name,'rb') as row_file:
            row_posses = pickle.load(row_file) 
            fetched[row] = row_posses
            row_patterns.append(row_posses)

print(len(row_patterns),'rows fetched')
a = solve(row_patterns,7)
print('\nSolution:')
for el in a:
    print(''.join(['.' if x == 0 else '#' for x in el]))
print('\n')

end_time = datetime.now()
runtime_in_seconds = (end_time - start_time).seconds
print(f'Finished at {end_time.strftime("%H:%M:%S")}')
print(f'Total time, {runtime_in_seconds} sec')
