# Now that we've found all possible patterns for any given row,
# we can take multiple rows and then just need to find a path through their possiblities

# Here we go!
# After each row has been processed by `row_set_gen.py`, we'll pass the 
# possibilties to `find_grid_pattern` along with the row_length of our input
# `find_grid_pattern` will recursively search for mergable path through 
# that list, eventually returning a new list of ints constituting the found pattern 
def find_grid_pattern(row_len,poss_per_row_list, current_posses=None, prev_choices=[]):
    # if on first level, options aren't filtered yet, so just grab options for top row
    if len(prev_choices) == 0:
        a = poss_per_row_list[0]
        current_posses = [poss for poss_key in a for poss in a[poss_key]]

    # if reached bottom level (!!!), let's hope possiblities include one that can wrap to our first choice
    # if so, just return first option (SCRATCH THAT)
    if len(prev_choices) == len(poss_per_row_list) - 1:
        top_of_first_choice = prev_choices[0] >> row_len
        for el in current_posses:
            # !!! This is the (second) change to allow for a wrap-around board
            bottom_two_of_top_poss = el & (2**(row_len * 2) - 1)
            if bottom_two_of_top_poss != top_of_first_choice: continue
            yield format_results(prev_choices + [el], row_len)
    else:
        # iterate current options
        for top_poss in current_posses:
            # filter next set of possibilites:
            # possiblities are already sorted under their top x digits, 
            # so we only recurse with options that match our current top_poss's 
            # bottom x digits
            bottom_two_of_top_poss = top_poss & (2**(row_len * 2) - 1)
            if bottom_two_of_top_poss not in poss_per_row_list[len(prev_choices) + 1]: continue
            poss_next = poss_per_row_list[len(prev_choices) + 1][bottom_two_of_top_poss]
            
            yield from find_grid_pattern(row_len,poss_per_row_list, poss_next, prev_choices + [top_poss])
            # otherwise continue to next iteration of current_posses


# The hard work done, parse the result of `find_grid_pattern` into
# a 2D array of 1s and 0s, ready for JSONificiation
def format_results(grid_pattern, row_length):
    # !!! new version for wrap-around truncates result
    first = grid_pattern[1]
    # convert first row-integer into binary string for first 2 rows
    first_2_rows = format((first >> row_length), f'0{row_length * 2}b')
    # then turn them into arrays of 1s and 0s and begin result
    row1 = [int(char) for char in first_2_rows[1:row_length-1]]
    row2 = [int(char) for char in first_2_rows[row_length+1:-1]]
    result = [row1, row2]
    # add rest of the third row of the rest of the results in grid_pattern
    for row_trio in grid_pattern[1:-1]:
        # for these we only care about the final {row_length} digits
        third_row = row_trio & (2**row_length - 1)
        row_str = format(third_row, f'0{row_length}b')
        result.append([int(char) for char in row_str[1:-1]])

    return result

# returns fetched rows and number of rows fetched
def fetch_row_possiblities(input_grid, row_dict):
    all_poss_row_patterns = []
    for row in input_grid:
        row_name = ''.join([str(x) for x in row])
        all_poss_row_patterns.append(row_dict[row_name])
    return all_poss_row_patterns

# bring it all together, takes a 2D array (N x N) of desired pattern
# returns 2D array (N+2 x N+2) of prev state
def find_prev_state(input_grid, row_dict):
    row_length = len(input_grid[0])
    all_poss_row_patterns = fetch_row_possiblities(input_grid, row_dict)
    return find_grid_pattern(row_length + 2, all_poss_row_patterns)