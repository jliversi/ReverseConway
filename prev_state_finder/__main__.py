from sys import argv

from run_reverse_conway import find_prev_to_depth
from conway_io import load_input

if __name__ == "__main__":
    INITIAL_GRID = load_input()

    MAX_DEPTH = 10
    if len(argv) > 1:
        MAX_DEPTH = int(argv[1])

    ROW_DICT = dict()
    result = find_prev_to_depth(INITIAL_GRID, ROW_DICT, MAX_DEPTH)
