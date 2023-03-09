# Conway's Game of Life: Previous State Finder

Early in my programming/computer science journey, I became fascinated with [Conway's Game of Life](https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life). One problem I was particularly interested in solving was whether you could play the game "backwards". That is, given a state X, can you produce the previous state Y?

This project is a small terminal-based python app for finding those previous states. Given a 2D JSON array as input, it will output a 2D JSON array of a state which will create the input in 3 turns of Conway's Game of Life. (Specifically this project asssumes a wrapping board of size equal to the input, for reasons outlined in the "How it works" section).

For a sample of previous states calculated with this tool, [visit this site](https://www.jliversi.com/ReverseConwaySampleDisplay/). There you can see 7 examples of patterns for which I calculated states 3 turns in advance. Simply choose a pattern and run the game using the play button (or one turn at a time using the one step button). The site can also be used to conveniently create input patterns for this tool using the "Export pattern" button.

## How to use

To use this app,
- clone this repo
- create a 2D json array of the game of life pattern you want to produce ([this site can help](https://www.jliversi.com/ReverseConwaySampleDisplay/))
- paste the json array into `json/input.json`
- run `python prev_state_finder your_label` with a label for this pattern
- output patterns will be placed in `json/output/your_label/#.json` (where `#` is the number of steps back)

## How it works

The goal: given a pattern for time `t`, determine the (a) pattern for time `t - 1`.

Firstly, I tackled the smallest version of this problem: given a _cell X_ at time `t`, determine that same cell X at time `t - 1`.

The rules of Conway's Game of Life are as follows:
```
Any live cell with fewer than two live neighbours dies, as if by underpopulation.
Any live cell with two or three live neighbours lives on to the next generation.
Any live cell with more than three live neighbours dies, as if by overpopulation.
Any dead cell with exactly three live neighbours becomes a live cell, as if by reproduction.
```
this means that to determine a cell's next state, we need to know not only the cell's current state, but also the state of its neighbors.

Returning to our single cell version, this means the "previous" state we want to find actually needs to be size 3x3; just returning the previous state of cell X at time `t - 1` would be insufficient to produce it at `t`.
```
ex. live on next turn (3 of the possible 140)
x x .    . . x    . . .
x . .    . x x    x x .
. . .    . . x    . . x

ex. dead on next turn (3 of the possible 372)
x . .    x x x    x . .
. . .    x x x    . x .
. . x    x x x    . . .
```

The next version of the problem is solving it for a 1D line of cells. For example, given the pattern `x .` at time `t`, produce the surroundsing 3x4 of the previous state. The 3x4 will have two overlapping 3x3 blocks:
```
x x .        x . .         x x . .
x . .   +    . . .    =    x . . .
. . .        . . x         . . . x
```
and the center cells of that pattern, after a turn, will be `x .` (alive - dead). So finding the previous state for a line of cells is just a matter of finding N overlapping 3x3s. The trick for doing this efficently is representing each 3x3 as a binary integer in which digit represents whether a cell is alive or dead:
```
b876543210
8 5 2
7 4 1
6 3 0
```
Then determining if another 3x3 can overlap is simply a matter of determining if it is within a range of 8 using some bit shifting:
```python
def calc_right_neighbors(num):
    # right neighbors are easier because the bottom three bits are free
    # therefore can be represented as some range of length 8
    # to determine bottom bound:
        # bitwise AND with 63 to wipe top 3 bits, then bitshift 3
        # ex. ABCDEFGHI -> DEFGHI000
    neighbor_lower_bound = (num & 63) << 3
    return range(neighbor_lower_bound, neighbor_lower_bound + 8)
```
Now we can easily and efficently produce a 3x(N + 2) at `t-1` for a given 1xN at `t`, we can repeat our previous strategy in the other dimension to get 2D results (though with significantly less efficiency as our binary numbers are now in _much_ larger ranges than 0-511 of our 3x3s).

One important note I've neglected to mention: each step you go back in time means producing a pattern 2 larger in each dimension. This is because a cell's state is affected by its neighbors, who's states themselves are determined by _their_ neighbors. This leads to each step farther back in time being a larger and larger problem to solve. To combat this and be capable of generating states farther in the past, I focused on a "wrapping" version of the game of life. This means the edges of the input are considered to wrap around to the opposite edge. (This can also be conceptualized as the shown pattern repeating infinitely in all directions). The only change this has for the algorithm is that after finding the last "neighbor 3x3", we need to make sure it's one which can connect back to our first "neighbor 3x3".

## Future Implementations
* Improve algorithm to merge larger blocks
* Implement parallelism using Python's `threading` library
* Calculate patterns for digital clock time display 