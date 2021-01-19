from row_patterns import ROW_PATTERNS
# BIG REFACTOR, STORE POSSIBLE 9s AS BINARY INTEGERS 



# Get all variations of 3x3, sort into way they affect next state of center cell

POSSIBLE_9S = []

for a in [0,1]:
    for b in [0,1]:
        for c in [0,1]:
            for d in [0,1]:
                for e in [0,1]:
                    for f in [0,1]:
                        for g in [0,1]:
                            for h in [0,1]:
                                for i in [0,1]:
                                    POSSIBLE_9S.append((a,b,c,d,e,f,g,h,i))

CENTER_ALIVE_AFTER = []
CENTER_DEAD_AFTER = []
KILLS_CENTER = []
REVIVES_CENTER = []

for poss in POSSIBLE_9S:
    center = poss[4]
    on_count = poss.count(1)
    if center:
        on_count -= 1
        if on_count in (2,3):
            CENTER_ALIVE_AFTER.append(poss)
        else:
            CENTER_DEAD_AFTER.append(poss)
            KILLS_CENTER.append(poss)
    else:
        if on_count == 3:
            CENTER_ALIVE_AFTER.append(poss)
            REVIVES_CENTER.append(poss)
        else:
            CENTER_DEAD_AFTER.append(poss)


    
# First goal, for each variation of a 1x3 grid:
    # produce a 3x5 grid which will next turn become 1x3



MERGE_9S_DICT_BASIC = dict()

def can_merge_9s(left, right):
    if left not in MERGE_9S_DICT_BASIC:
        MERGE_9S_DICT_BASIC[left] = []
    elif right in MERGE_9S_DICT_BASIC[left]:
        return True
    
    if left[2] == right[1] and left[5] == right[4] and left[8] == right[7] and left[1] == right[0] and left[4] == right[3] and left[7] == right[6]:
        MERGE_9S_DICT_BASIC[left].append(right)
        return True
    else:
        return False

for el1 in POSSIBLE_9S:
    for el2 in POSSIBLE_9S:
        can_merge_9s(el1, el2)

MERGE_9S_DICT = dict()

for k in MERGE_9S_DICT_BASIC:
    MERGE_9S_DICT[k] = {'on': set(), 'off': set()}
    on_arr = MERGE_9S_DICT[k]['on']
    off_arr = MERGE_9S_DICT[k]['off']
    for el in MERGE_9S_DICT_BASIC[k]:
        if el in CENTER_ALIVE_AFTER:
            on_arr.add(el)
        else:
            off_arr.add(el)

# for k in MERGE_9S_DICT:
#     print(k)
#     print(MERGE_9S_DICT[k])
#     print('\n\n')


ONS_WITH_NEXT_ONS = []
ONS_WITH_NEXT_OFFS = []
OFFS_WITH_NEXT_ONS = []
OFFS_WITH_NEXT_OFFS = []

for k in MERGE_9S_DICT:
    ons, offs = MERGE_9S_DICT[k]['on'], MERGE_9S_DICT[k]['off']
    if k in CENTER_ALIVE_AFTER:
        if len(ons): ONS_WITH_NEXT_ONS.append(k)
        if len(offs): ONS_WITH_NEXT_OFFS.append(k)
    else:
        if len(ons): OFFS_WITH_NEXT_ONS.append(k)
        if len(offs): OFFS_WITH_NEXT_OFFS.append(k)


def find_all_sets_no_grid(row):
    # recursive method, called on each smaller piece of row
    
    # base case, return on and off options for last cell
    if len(row) == 1:
        return list(map(lambda x: [x], CENTER_ALIVE_AFTER)) if row[0] else list(map(lambda x: [x], CENTER_DEAD_AFTER))
    
    # recursive call, get all options minus first cell
    prev_step = find_all_sets_no_grid(row[1:])
    prev_step_last_els = set([x[0] for x in prev_step])
    current = row[0]
    next_cell = row[1]
    result = []
    if current and next_cell:
        options = ONS_WITH_NEXT_ONS
        for el1 in options:
            for el2 in MERGE_9S_DICT[el1]['on']:
                if el2 in prev_step_last_els:
                    prev_step_rows = [x for x in prev_step if x[0] == el2]
                    for prev_row in prev_step_rows:
                        result.append([el1] + prev_row)

    elif current and not next_cell:
        options = ONS_WITH_NEXT_OFFS
        for el1 in options:
            for el2 in MERGE_9S_DICT[el1]['off']:
                if el2 in prev_step_last_els:
                    prev_step_rows = [x for x in prev_step if x[0] == el2]
                    for prev_row in prev_step_rows:
                        result.append([el1] + prev_row)

    elif not current and next_cell:
        options = OFFS_WITH_NEXT_ONS
        for el1 in options:
            for el2 in MERGE_9S_DICT[el1]['on']:
                if el2 in prev_step_last_els:
                    prev_step_rows = [x for x in prev_step if x[0] == el2]
                    for prev_row in prev_step_rows:
                        result.append([el1] + prev_row)

    else:
        options = OFFS_WITH_NEXT_OFFS
        for el1 in options:
            for el2 in MERGE_9S_DICT[el1]['off']:
                if el2 in prev_step_last_els:
                    prev_step_rows = [x for x in prev_step if x[0] == el2]
                    for prev_row in prev_step_rows:
                        result.append([el1] + prev_row)

    return result

# get set of "9"s into a 3x5 array
def conact_9s(*nines):
    first = list(nines[0])
    nines = nines[1:]
    result = [
        first[0:3],
        first[3:6],
        first[6:9]
    ]
    for el in nines:
        result[0].append(el[2])
        result[1].append(el[5])
        result[2].append(el[8])
    return result
        
def find_all_sets(row):
    return [sum(el,()) for el in find_all_sets_no_grid(row)]
    # return [conact_9s(*el) for el in find_all_sets_no_grid(row)]

def concat_9_tuples(three_nine_tuple):
    first = list(three_nine_tuple[0:9])
    nines = []
    nines.append(three_nine_tuple[9:18])
    nines.append(three_nine_tuple[18:27])
    result = [
        first[0:3],
        first[3:6],
        first[6:9]
    ]
    for el in nines:
        result[0].append(el[2])
        result[1].append(el[5])
        result[2].append(el[8])
    return result

MERGE_3X5_DICT = dict()

def can_merge_3x5s(left, right):
    if left not in MERGE_3X5_DICT:
        MERGE_3X5_DICT[left] = []
    elif right in MERGE_3X5_DICT[left]:
        return True 

    if left[3:5] == right[0:2] and left[8:10] == right[5:7] and left[13:15] == right[10:12]:
        MERGE_3X5_DICT[left].append(right)
        return True
    else:
        return False

def merged_3by5s(left, right):
    left_arr = concat_9_tuples(left)
    right_arr = concat_9_tuples(right)
    result = []
    for l, r in zip(left_arr, right_arr):
        new_row = l + r[2:]
        result.append(new_row)
    return result

def merged_3byXs(left, right):
    right_arr = concat_9_tuples(right)
    result = []
    for l, r in zip(left, right_arr):
        new_row = l + r[2:]
        result.append(new_row)
    return result

ALL_3S = (
    (0,1,1),
    (0,1,0),
    (0,0,1),
    (0,0,0),
    (1,1,1),
    (1,1,0),
    (1,0,1),
    (1,0,0),
)

SETS_PER_3 = dict()
for el in ALL_3S:
    SETS_PER_3[el] = find_all_sets(el)


def find_all_for_21_row(row):
    one, two, three, four, five, six, seven = [SETS_PER_3[x] for x in row]
    for a in one:
        for b in two:
            if can_merge_3x5s(a,b):
                for c in three:
                    if can_merge_3x5s(b,c):
                        for d in four:
                            if can_merge_3x5s(c,d):
                                for e in five:
                                    if can_merge_3x5s(d,e):
                                        for f in six:
                                            if can_merge_3x5s(e,f):
                                                for g in seven:
                                                    if can_merge_3x5s(f,g):
                                                        yield [a,b,c,d,e,f,g]

def merge_row_results(row_results):
    merged = merged_3by5s(row_results[0],row_results[1])
    for el in row_results[2:]:
        merged = merged_3byXs(merged, el)
    return merged

def can_merge_rows(top, bottom):
    return top[1] == bottom[0] and top[2] == bottom[1]

def print_grid(grid):
    for el in grid:
        print(el)

row1_gen, row2_gen, row3_gen, row4_gen, row5_gen = [find_all_for_21_row(x) for x in ROW_PATTERNS]

found = False 
for a in row1_gen:
    if found: break
    a = merge_row_results(a)
    for b in row2_gen:
        if found: break
        b = merge_row_results(b)
        if can_merge_rows(a,b):
            print('checking for 3rd')
            for c in row3_gen:
                if found: break
                c = merge_row_results(c)
                if can_merge_rows(b,c):
                    print('checking for 4th')
                    for d in row4_gen:
                        if found: break
                        d = merge_row_results(d)
                        if can_merge_rows(c,d):
                            print('checking for 5th!!!!!')
                            for e in row5_gen:
                                if found: break
                                e = merge_row_results(e)
                                if can_merge_rows(d,e):
                                    found = True
                                    print_grid(a)
                                    print_grid(b)
                                    print_grid(c)
                                    print_grid(d)
                                    print_grid(e)
                            


# for k in SETS_PER_3:
#     print(k, ':', len(SETS_PER_3[k]))

# print('----')

# for x in [find_all_for_21_row(x) for x in ROW_PATTERNS]:
#     i = 0
#     for y in x:
#         i+= 1
#     print(i)