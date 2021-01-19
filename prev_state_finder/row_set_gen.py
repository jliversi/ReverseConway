import json
import pickle
import os.path

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


def sqrs_to_rows(num_list):
    # first, determine the total number of bits needed
    total_bits = 3 * len(num_list) + 6
    row_len = total_bits // 3
    # build up each row, starting with first 2 cols of num_list[0]
    first = num_list[0]
    row1 = (2 * nth_bin_dig(first, 8)) + nth_bin_dig(first, 5)
    row2 = (2 * nth_bin_dig(first, 7)) + nth_bin_dig(first, 4)
    row3 = (2 * nth_bin_dig(first, 6)) + nth_bin_dig(first, 3)
    rows = [row3, row2, row1]
    # then add on additional digits
    for num in num_list:
        for i in range(3):
            rows[i] = (rows[i] << 1) + nth_bin_dig(num,i)

    # build final result
    result = rows[0]
    result += rows[1] << row_len
    result += rows[2] << (row_len * 2)
    return result


# everything so far comes together here
# takes a row pattern of ONs and OFFs (iterable of truthy/falsey)
# returns a list of possible 3xNs, as returned by `sqrs_to_rows`
# Strategy: recursively loop through possiblities, restricting search space
# in each step to neighbors of previous step (except first which is all ONs or OFFs)
def poss_row_patterns(row, cur_idx=0, prev_cells=[]):
    if cur_idx > 0:
        # determine next set and store in `next_cells`
        on_or_off = 'ON' if row[cur_idx] else 'OFF'
        next_cells = NBR_DICT[prev_cells[-1]][on_or_off]

        # base case, if on final cell, yield a each poss pattern from this chain
        if cur_idx == len(row) - 1:
            for next_cell in next_cells:
                yield sqrs_to_rows(prev_cells + [next_cell])
        # otherwise continue the chain
        else:
            for next_cell in next_cells:
                yield from poss_row_patterns(row, cur_idx + 1, prev_cells + [next_cell])
    else: 
        # if on first cell, start with all of OFF or all of ON
        next_cells = ON if row[0] else OFF
        for next_cell in next_cells:
            yield from poss_row_patterns(row, cur_idx + 1, [next_cell])


# Run it 
with open('i_o/input.json') as f:
    input_grid = json.load(f)


for i, row in enumerate(input_grid):
    row_name = ''.join([str(x) for x in row])
    print(f'Processing {row_name}')
    file_name = f'obj_files/{row_name}.obj'
    if os.path.isfile(file_name):
        print(f'File for {row_name} already exists')
        continue

    result = [x for x in poss_row_patterns(row)]
    # sort here by top n digts 
    row_len = len(row) + 2
    tops_dict = dict()
    for num in result:
        top = num >> row_len
        if top in tops_dict:
            tops_dict[top].append(num)
        else:
            tops_dict[top] = [num]

    print(f'Pickling {len(result)} possible patterns into {file_name}\n')
    with open(file_name, 'xb') as row_file:
        pickle.dump(tops_dict, row_file)

















# TESTS START HERE
# TESTS START HERE
# TESTS START HERE
# TESTS START HERE
# TESTS START HERE
# TESTS START HERE


# For testing times

# from datetime import datetime

# start_time = datetime.now()
# print('Start time: ',start_time.strftime("%H:%M:%S"),'\n')
# with open('pattern.txt') as f:
#     INPUTS = [line.replace('\n','') for line in f]

# for i, row in enumerate(INPUTS):
#     print(f'Processing {row} ({len(row)})')
#     file_name = f'obj_files/{row}.obj'
#     if os.path.isfile(file_name):
#         print(f'{file_name} already exists')
#         continue
#     row_list = list(map(lambda x: x == '1', row))
#     row_start_time = datetime.now()
#     result = [x for x in poss_row_patterns(row_list)]
#     dur1 = (datetime.now() - row_start_time).seconds
#     print(f'All patterns found in {dur1} seconds')
#     # Sorting by top 2 rows
#     tops_dict = dict()
#     for el in result:
#         top = el[:2]
#         if top in tops_dict:
#             tops_dict[top].append(el)
#         else:
#             tops_dict[top] = [el]

#     dur2 = (datetime.now() - row_start_time).seconds
#     print(f'All patterns sorted by top 2 in {dur2 - dur1} seconds')
#     print(f'Dumping {len(result)} patterns')
#     with open(file_name, 'xb') as row_file:
#         pickle.dump(tops_dict, row_file)
#     print(f'Total time for {row}: {dur2} seconds')
#     print('\n')

    

# end_time = datetime.now()
# runtime_in_seconds = (end_time - start_time).seconds
# print(f'Total time, {runtime_in_seconds} sec')




# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE
# LEGACY STARTS HERE




# OLD NON-GEN VERSION! WITH COMMENTS
# everything so far comes together here
# takes a row pattern of ONs and OFFs (iterable of truthy/falsey)
# returns a list of possible 3xNs, as returned by `sqr_ints_to_row_ints`
# Strategy: recursively loop through possiblities, restricting search space
# in each step to neighbors of previous step (except first which is all ONs or OFFs)
# def poss_row_patterns(row, prev_cell=None):
#     results = []
#     if prev_cell != None:
#         # get neighbors form NBR_DICT cache
#         next_cells = NBR_DICT[prev_cell]['ON'] if row[0] else NBR_DICT[prev_cell]['OFF']
#         # base case, on last element
#         if len(row) == 1:
#             for next_cell in next_cells:
#                 results.append([prev_cell, next_cell])
#         else:
#             for next_cell in next_cells:
#                 for ele in poss_row_patterns(row[1:], next_cell):
#                     results.append([prev_cell] + ele) # way too much concatting on this line
#     else:
#         # for first cell, filter to all ONs or all OFFs
#         next_cells = ON if row[0] else OFF
#         for next_cell in next_cells:
#                 for ele in poss_row_patterns(row[1:], next_cell):
#                     results.append(ele)

#     # keep sending up intermediate results unless at top level
#     if prev_cell != None:
#         return results
#     else:
#         return list(map(sqr_ints_to_row_ints, results))





# THIS BECAME `sqrs_to_rows`

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
# def sqr_ints_to_row_ints(num_list):
#     # Strategy: build up each row as a sum of powers of 2
#     # Start with first num, the only 3x3 you take all of, get first 2 cols
#     first = num_list[0]
#     row1 = nth_bin_dig(first, 8) + (2 * nth_bin_dig(first, 5))
#     row2 = nth_bin_dig(first, 7) + (2 * nth_bin_dig(first, 4))
#     row3 = nth_bin_dig(first, 6) + (2 * nth_bin_dig(first, 3))

#     # then add on additional powers of 2
#     cur_exp = 2 # 1s and 2s place already built
#     for num in num_list:
#         row1 += (2**cur_exp) * nth_bin_dig(num,2)
#         row2 += (2**cur_exp) * nth_bin_dig(num,1)
#         row3 += (2**cur_exp) * nth_bin_dig(num,0)
#         cur_exp += 1

#     return (row1, row2, row3)