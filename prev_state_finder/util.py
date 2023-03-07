import json
from datetime import datetime

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

# Display methods, for testing
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