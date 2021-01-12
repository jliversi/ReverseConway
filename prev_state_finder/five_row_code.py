# represent 7x3 grids as rows, each of which is a num between 0 and 127
class FiveRow:
    def __init__(self, num_list):
        self.parse_input(num_list)

    def parse_input(self, num_list):
        # formats number as a 9 digit binary string
        first = format(num_list[0], '09b')
        row1 = first[0] + first[3] + first[6]
        row2 = first[1] + first[4] + first[7]
        row3 = first[2] + first[5] + first[8]
        for num in num_list[1:]:
            num = format(num, '09b')
            row1 += num[6]
            row2 += num[7]
            row3 += num[8]
        self.row1 = int(row1, 2)
        self.row2 = int(row2, 2)
        self.row3 = int(row3, 2)
    
    def print_self(self):
        print(format(self.row1, '07b'))
        print(format(self.row2, '07b'))
        print(format(self.row3, '07b'))
