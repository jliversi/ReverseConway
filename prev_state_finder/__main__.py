from sys import argv
import os

from run_reverse_conway import find_prev_to_depth
from conway_io import load_input

if __name__ == "__main__":
    INITIAL_GRID = load_input()

    if len(argv) < 2:
        print("Please provide a label for this output")
        quit()

    LABEL = argv[1]
    dir_name = f'{os.getcwd()}/json/output/{LABEL}'
    if not os.path.isdir(dir_name):
        os.mkdir(dir_name)

    MAX_DEPTH = 3
    if len(argv) > 2:
        MAX_DEPTH = int(argv[2])

    ROW_DICT = dict()
    result = find_prev_to_depth(INITIAL_GRID, ROW_DICT, MAX_DEPTH, LABEL)
