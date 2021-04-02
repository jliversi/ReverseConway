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