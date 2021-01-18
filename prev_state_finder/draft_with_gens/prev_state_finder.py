# TODO: Refactor poss_row_patterns to not do so much partial list concatting....
# !!!!!! REFACTOR TO BECOME A GENERATOR!
# which will likely mean refactoring `find_grid_pattern`.....
# TODO: create seperate file for running it, importing solve, change format of output (this should be determined by how you want your JS to take it)




# Step 1, pre-process all possible 3x3 grids, for each determine:
# 1. Whether the center cell is ON or OFF in next gen
# 2. All possible merge-able right neighbors (sorted by prev property)

# To do this, represent each 3x3 as a binary number btwn 0 and 511
# each digit represents whether a cell is full
# b876543210
# 8 5 2
# 7 4 1
# 6 3 0

# helper function, appropriately named (counts from right, starting at 0, b876543210)
def nth_bin_dig(num, n):
    return (num >> n) & 1

# Determine center cell of next gen (True for OFF, False for OFF)
def next_gen_center(num):
    # determine middle bit (currently OFF or OFF)
    mid_bit = nth_bin_dig(num, 4)
    # clever solution for finding num set bits in bin int (credit: Brian Kernighan)
    count = 0
    n = num
    while n:
        n = n & (n-1)
        count += 1
    # all of the rules of conway happen here
    if (mid_bit and count in [3,4]) or (not mid_bit and count == 3):
        return True
    else:
        return False

# Sort ints btwn 0 and 512 into those which leave on, or leave off
ON = []
OFF = []
for i in range(512):
    ON.append(i) if next_gen_center(i) else OFF.append(i)

# key insight here: representing 3x3s as binary integers means we can
    # determine potential right neighbors as ranges
def calc_right_neighbors(num):
    # right neighbors are easier because the bottom three bits are free
    # therefore can be represented as some range of length 8
    # to determine bottom bound:
        # bitwise AND with 63 to wipe top 3 bits, then bitshift 3
        # ex. ABCDEFGHI -> DEFGHI000
    neighbor_lower_bound = (num & 63) << 3
    return range(neighbor_lower_bound, neighbor_lower_bound + 8)


# Associate each 3x3 int with its possible ON and OFF right neighbors
NBR_DICT = dict()
for i in range(512):
    nbr_range = calc_right_neighbors(i)
    on_nbrs, off_nbrs = [], []
    for nbr in nbr_range:
        on_nbrs.append(nbr) if next_gen_center(nbr) else off_nbrs.append(nbr)
    NBR_DICT[i] = {'ON': tuple(on_nbrs), 'OFF': tuple(off_nbrs)}


# After we find mergable sets of 3x3s (horizontal matches per row), we'll want 
# 3-row objects for finding vertical matches.
# `sqr_ints_to_row_ints` Takes a list of n integers representing 3x3 sqrs
# return 3 integers representing the rows produced after merged. Ex.
# input: (81,    137,    72) (a possible solution to ON-ON-OFF)
#       0 0 0   0 0 0   0 0 0   --overlap&reversed--> 00000 --> 0
#       0 1 0   1 0 0   0 0 0   --overlap&reversed--> 00010 --> 2
#       1 0 1   0 1 1   1 1 0   --overlap&reversed--> 01101 --> 13
# output: (0,8,22)
# result ints will fall in range 0 - (2**(n+2)) (n is length of input)
# this range doesn't really matter though, as long as consistent for grid input
# (results also end up reversed to make iterative logic simpler, unreversed on eventual print)
def sqr_ints_to_row_ints(num_list):
    # Strategy: build up each row as a sum of powers of 2
    # Start with first num, the only 3x3 you take all of, get first 2 cols
    first = num_list[0]
    row1 = nth_bin_dig(first, 8) + (2 * nth_bin_dig(first, 5))
    row2 = nth_bin_dig(first, 7) + (2 * nth_bin_dig(first, 4))
    row3 = nth_bin_dig(first, 6) + (2 * nth_bin_dig(first, 3))

    # then add on additional powers of 2
    cur_exp = 2 # 1s and 2s place already built
    for num in num_list:
        row1 += (2**cur_exp) * nth_bin_dig(num,2)
        row2 += (2**cur_exp) * nth_bin_dig(num,1)
        row3 += (2**cur_exp) * nth_bin_dig(num,0)
        cur_exp += 1

    return (row1, row2, row3)










# everything so far comes together here
# takes a row pattern of ONs and OFFs (iterable of truthy/falsey)
# returns a list of possible 3xNs, as returned by `sqr_ints_to_row_ints`
# Strategy: recursively loop through possiblities, restricting search space
# in each step to neighbors of previous step (except first which is all ONs or OFFs)

# TODO: Rewrite ^^ explanation after having refactored to gens



# TIME TO MAKE THIS BAD BOY A GEN! 
def poss_row_patterns(input_row):

    def _row_gen(row=input_row, cur_idx=0, prev_cells=[]):
            if cur_idx > 0:
                on_or_off = 'ON' if row[cur_idx] else 'OFF'
                next_cells = NBR_DICT[prev_cells[-1]][on_or_off]
                if cur_idx == len(row) - 1:
                    for next_cell in next_cells:
                        yield sqr_ints_to_row_ints(prev_cells + [next_cell])
                else:
                    for next_cell in next_cells:
                        yield from _row_gen(row, cur_idx + 1, prev_cells + [next_cell])
            else: 
                next_cells = ON if row[0] else OFF
                for next_cell in next_cells:
                    yield from _row_gen(row, cur_idx + 1, [next_cell])
    return _row_gen






















# Now that we can find all possible patterns for any given row,
# we can take multiple rows and then just need to find a path through their possiblities

# First, a couple of helper functions
# takes two 3-row-integer-tuples, returns boolean indicating if they can be merged
def can_merge(t,b):
    return t[1] == b[0] and t[2] == b[1]

# for a given top and a set of possible bottoms, filter for mergable
def filter_poss_bottoms(top, bottoms):
    return filter(lambda x: can_merge(top,x),bottoms())

# Here we go!
# After passing each row into through `poss_row_patterns`, collect results in list
# pass that list to solve, will recursively search for mergable path through that list
# returns a list of three-row-integer-tuples
def find_grid_pattern(poss_per_row_list, current_posses=None, depth=0):
    # if on first level, options aren't filtered yet, so just grab first set
    if depth == 0:
        current_posses = poss_per_row_list[0]()

    # if reached bottom level (!!!), let's hope possiblities are non-empty...
    # if so, just return first option
    if depth == len(poss_per_row_list) - 1:
        for el in current_posses:
            return [el]

    # iterate current options
    for top in current_posses:
        # filter next set of possibilites
        poss_next = filter_poss_bottoms(top, poss_per_row_list[depth + 1])
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
def solve(input_grid):
    print("Finding partial solutions per row...")
    all_poss_row_patterns = list(map(poss_row_patterns, input_grid))
    print("Searching for full solution...")
    found_pattern = find_grid_pattern(all_poss_row_patterns)
    print("Formatting results...")
    return format_results(found_pattern, len(input_grid[0]) + 2)



# DELETE AFTER HERE

with open('test_pattern.txt') as f:
    INPUTS = [list(map(lambda x: x == '#', line.replace('\n',''))) for line in f]


# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE
# DELETE AFTER HERE








from datetime import datetime

def print_now():
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(current_time)

print_now()
for el in solve(INPUTS):
    print(el)
print_now()


# for el in INPUTS:
#     posses = poss_row_patterns(el)
#     count = 0
#     for el2 in posses:
#         count += 1
#     print(count) 
#     print_now()

# Takes 8 minutes to produce all possible 7-empty row patterns
# there are 22,406,933 patterns, and they take 200MB to store




# if __name__ == "__main__":
if False:
    from timeit import timeit
    with open('test_pattern.txt') as f:
        INPUTS = [list(map(lambda x: x == '#', line.replace('\n',''))) for line in f]

    # def do_it():
    #     solution = solve(INPUTS)
    #     for el in solution:
    #         print(el)
    # print('old code', timeit('do_it()',globals=locals(), number=1))

    # generator test 
    def poss_row_patterns(row):
        def _row_gen():
            one = ON if row[0] else OFF
            for a in one:
                two = NBR_DICT[a]['ON'] if row[1] else NBR_DICT[a]['OFF']
                for b in two:
                    three = NBR_DICT[b]['ON'] if row[2] else NBR_DICT[b]['OFF']
                    for c in three:
                        four = NBR_DICT[c]['ON'] if row[3] else NBR_DICT[c]['OFF']
                        for d in four:
                            five = NBR_DICT[d]['ON'] if row[4] else NBR_DICT[d]['OFF']
                            for e in five:
                                six = NBR_DICT[e]['ON'] if row[5] else NBR_DICT[e]['OFF']
                                for f in six:
                                    seven = NBR_DICT[f]['ON'] if row[6] else NBR_DICT[f]['OFF']
                                    for g in seven:
                                        yield sqr_ints_to_row_ints((a,b,c,d,e,f,g))
        return _row_gen

    # IMPORTANT DIFF HERE, INVOKING BOTTOM
    def filter_poss_bottoms(top, bottoms):
        return filter(lambda x: can_merge(top,x),bottoms())


    # Ummmmmmm is this the same?
    # def find_grid_pattern(poss_per_row_list, current_posses=None, level=0):
    #     if level == 0:
    #         current_posses = poss_per_row_list[0]()

    #     # if reached bottom level with possiblities (!!!), just return first option
    #     if level == len(poss_per_row_list) - 1:
    #         return [next(current_posses)]

    #     # iterate current options
    #     for top in current_posses:
    #         # filter next set of possibilites
    #         poss_next = filter_poss_bottoms(top, poss_per_row_list[level + 1])
    #         # if there are possiblities, recurse with those possibilties
    #         if poss_next:
    #             subresult = find_grid_pattern(poss_per_row_list, poss_next, level + 1)
    #             # if subresult is truthy, we found it! send it up!!!!
    #             if subresult:
    #                 return [top] + subresult
    #             # otherwise continue to next iteration of current_posses

    #     # if never found, return None for recursive results
    #     return None

    def solve(input_grid):
        print("Finding partial solutions per row...")
        all_poss_row_patterns = list(map(poss_row_patterns, input_grid))
        print("Searching for full solution...")
        found_pattern = find_grid_pattern(all_poss_row_patterns)
        print("Formatting results...")
        return format_results(found_pattern, len(input_grid[0]) + 2)

    def do_it():
        solution = solve(INPUTS)
        for el in solution:
            print(el)
    print('new code', timeit('do_it()',globals=locals(), number=1))










    # def loop_six(row):
    #     results = []
    #     one = ON if row[0] else OFF
    #     for a in one:
    #         two = NBR_DICT[a]['ON'] if row[1] else NBR_DICT[a]['OFF']
    #         for b in two:
    #             three = NBR_DICT[b]['ON'] if row[2] else NBR_DICT[b]['OFF']
    #             for c in three:
    #                 four = NBR_DICT[c]['ON'] if row[3] else NBR_DICT[c]['OFF']
    #                 for d in four:
    #                     five = NBR_DICT[d]['ON'] if row[4] else NBR_DICT[d]['OFF']
    #                     for e in five:
    #                         six = NBR_DICT[e]['ON'] if row[5] else NBR_DICT[e]['OFF']
    #                         for f in six:
    #                             results.append(sqr_ints_to_row_ints((a,b,c,d,e,f)))
    #     return results

    # def loop_seven(row):
    #     results = []
    #     one = ON if row[0] else OFF
    #     for a in one:
    #         two = NBR_DICT[a]['ON'] if row[1] else NBR_DICT[a]['OFF']
    #         for b in two:
    #             three = NBR_DICT[b]['ON'] if row[2] else NBR_DICT[b]['OFF']
    #             for c in three:
    #                 four = NBR_DICT[c]['ON'] if row[3] else NBR_DICT[c]['OFF']
    #                 for d in four:
    #                     five = NBR_DICT[d]['ON'] if row[4] else NBR_DICT[d]['OFF']
    #                     for e in five:
    #                         six = NBR_DICT[e]['ON'] if row[5] else NBR_DICT[e]['OFF']
    #                         for f in six:
    #                             seven = NBR_DICT[f]['ON'] if row[6] else NBR_DICT[f]['OFF']
    #                             for g in seven:
    #                                 results.append(sqr_ints_to_row_ints((a,b,c,d,e,f,g)))
    #     return results

    # print('Hardcoded loop functions:')
    # print('5 loop', timeit('loop_five((0,1,1,0,1))', globals=locals(), number=5))
    # print('6 loop', timeit('loop_six((0,1,1,0,1,0))', globals=locals(), number=5))
    # print('7 loop', timeit('loop_seven((0,1,1,0,1,0,0))', globals=locals(), number=5))
    # print('-----')
    # print('3 inputs', timeit('poss_row_patterns((0,1,1))', globals=locals(), number=5))
    # print('4 inputs', timeit('poss_row_patterns((0,1,1,0))', globals=locals(), number=5))
    # print('5 inputs', timeit('poss_row_patterns((0,1,1,0,1))', globals=locals(), number=5))
    # print('6 inputs', timeit('poss_row_patterns((0,1,1,0,1,0))', globals=locals(), number=5))
    # print('7 inputs', timeit('poss_row_patterns((0,1,1,0,1,0,0))', globals=locals(), number=5))