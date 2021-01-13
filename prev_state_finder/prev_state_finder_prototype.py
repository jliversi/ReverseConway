import timeit

with open('pattern.txt') as f:
    INPUTS = [list(map(lambda x: x == '#', line)) for line in f]
# represent each 3x3 as a binary number btwn 0 and 511
# each digit represents whether a square is full 
# b876543210
# 8 5 2
# 7 4 1
# 6 3 0
class BinSqr:
    # dict to access a square from an int
    SQRS = dict()
    # lists of nums corresponding to BinSqrs with next_on props on or off 
    ON = []
    OFF = []

    def __init__(self, num):
        self.num = num
        self.num_on = self.num_set_bits()
        mid_bit = (num & 16) >> 4
        # all of the rules of conway happen here
        if (mid_bit and self.num_on in [3,4]) or (not mid_bit and self.num_on == 3):
            self.next_on = True
            BinSqr.ON.append(num)
        else:
            BinSqr.OFF.append(num)
            self.next_on = False 

        self.calc_right_neighbors()
        BinSqr.SQRS[num] = self
    
    # clever solution for finding num set bits in bin int (credit: Brian Kernighan)
    def num_set_bits(self):
        count = 0
        n = self.num
        while n:
            n = n & (n-1)
            count += 1
        return count

    # key insight here: can determine potential right neighbors as ranges
    def calc_right_neighbors(self):
        # right neighbors are easier because the bottom bits are free
        # right lower bound
        # bitwise AND with 63 to wipe top 3 bits, bitshift 3
        # ABCDEFGHI -> DEFGHI000
        rlb = (self.num & 63) << 3
        self.right_neighbors = range(rlb, rlb + 8)
        # left neighbors are a bit tougher 
        # they are multiples of 64 greater starting at (self.num >> 3)
        # ignoring for now, probably can just build left to right
        # update: turns out i could get away with building left to right :) 

    def calc_on_and_off_neighbors(self):
        self.on_right_neigbors = [x for x in self.right_neighbors if x in BinSqr.ON]
        self.off_right_neigbors = [x for x in self.right_neighbors if x not in BinSqr.ON]

# create and setup all possible squares
for i in range(512):
    BinSqr(i)
for i in range(512):
    BinSqr.SQRS[i].calc_on_and_off_neighbors()


# takes list of 5 integers, each representing a BinSqr nine
# returns tuple of 3 ints, each a 7 bit on-off row (top -> bottom)
def convert_5x1_3x7(num_list):
    first = format(num_list[0], '09b')
    row1 = first[0] + first[3] + first[6]
    row2 = first[1] + first[4] + first[7]
    row3 = first[2] + first[5] + first[8]
    for num in num_list[1:]:
        num = format(num, '09b')
        row1 += num[6]
        row2 += num[7]
        row3 += num[8]
    return (int(row1, 2), int(row2, 2), int(row3, 2))

# takes a tuple of 7 bit integers, prints the rows each represents
def print_3x7(row_tuple):
    print(format(row_tuple[0], '07b'))
    print(format(row_tuple[1], '07b'))
    print(format(row_tuple[2], '07b'))



# takes in a tuple containing 5 Truthys's or Falsey's
# returns a tuple of integers, each integer representing a 7 bit on-off row (this isnt even true lol)
def poss_1x5_patterns(row):
    results = []
    one = BinSqr.ON if row[0] else BinSqr.OFF
    for a in one:
        a_sqr = BinSqr.SQRS[a]
        two = a_sqr.on_right_neigbors if row[1] else a_sqr.off_right_neigbors
        for b in two:
            b_sqr = BinSqr.SQRS[b]
            three = b_sqr.on_right_neigbors if row[2] else b_sqr.off_right_neigbors
            for c in three:
                c_sqr = BinSqr.SQRS[c]
                four = c_sqr.on_right_neigbors if row[3] else c_sqr.off_right_neigbors
                for d in four:
                    d_sqr = BinSqr.SQRS[d]
                    five = d_sqr.on_right_neigbors if row[4] else d_sqr.off_right_neigbors
                    for e in five:
                        results.append(convert_5x1_3x7((a,b,c,d,e)))
    return results

print("Finding partial solutions per row...")
# possibilites_per_line = [poss_1x5_patterns(l) for l in INPUTS]
# timeit.timeit('possibilites_per_line = [poss_1x5_patterns(l) for l in INPUTS]', globals=locals())

# takes two FiveRow objects, returns boolean indicating if they can be merged
def can_merge(t,b):
    return t[1] == b[0] and t[2] == b[1]

# for a given top and a set of possible bottoms, filter for mergable
def filter_poss_bottoms(top, bottoms):
    return list(filter(lambda x: can_merge(top,x),bottoms))

def recurse_possibilities(current_posses, level=0):
    # if reached bottom of tree, just return first option 
    if level == len(INPUTS) - 1:
        return [current_posses[0]]

    # iterate current options
    for top in current_posses:
        # filter next set of possibilites
        poss_next = filter_poss_bottoms(top, possibilites_per_line[level + 1])
        # if there are possiblities, recurse with those possibilties
        if len(poss_next):
            subresult = recurse_possibilities(poss_next, level + 1)
            # if subresult is truthy, we found it! continue it!
            if subresult:
                return [top] + subresult
            # otherwise continue to next iteration of current_posses
    
    # if never find, return None for recursive results
    return None


# Run the code, hope it works! 
# print("Searching for full solution...")
# a = recurse_possibilities(possibilites_per_line[0])

# # print the result!
# print(format(a[0][0], '07b'))
# print(format(a[0][1], '07b'))
# for el in a:
#     print(format(el[2], '07b'))






# # for testing
# def num_to_3x3(num):
#     print(num)
#     num = format(num, '09b')
#     print(num)
#     print(num[0],num[3],num[6])
#     print(num[1],num[4],num[7])
#     print(num[2],num[5],num[8])


if __name__ == "__main__":
    from timeit import timeit
    print('5 row')
    print(timeit('poss_1x5_patterns((0,1,1,0,1))', globals=locals(), number=10))
