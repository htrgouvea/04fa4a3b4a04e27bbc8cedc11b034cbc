# Challenge 1: Minesweeper Number of Neighbouring Mines

This folder contains the solution for Challenge 1.

Required file:

```text
solution_minesweeper.py
```

Required function signature:

```python
def count_neighbouring_mines(board: list) -> list:
```

The code uses Python 3.12, as required by the challenge.

## Problem

The input is a 2D list representing a Minesweeper board:

- `0` means an empty cell.
- `1` means a mine.

The output must be another 2D list with the same dimensions:

- Mine cells become `9`.
- Empty cells become the number of mines in their neighbouring cells.

A cell can have up to eight neighbours:

```text
top-left     top     top-right
left         cell    right
bottom-left  bottom  bottom-right
```

## Algorithm

The solution follows these steps:

1. Create a result board with the same size as the input board.
2. Visit each cell in the board.
3. If the current cell is a mine, write `9` in the result board.
4. If the current cell is empty, inspect all eight possible neighbouring positions.
5. Ignore neighbouring positions that fall outside the board.
6. Count how many valid neighbours contain a mine.
7. Write that count in the result board.

## Example

Input:

```python
[
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 1, 0, 0],
]
```

Output:

```python
[
    [1, 9, 2, 1],
    [2, 3, 9, 2],
    [3, 9, 4, 9],
    [9, 9, 3, 1],
]
```

## Why The Code Is Split Into Helpers

The challenge only requires `count_neighbouring_mines`, but the solution also
uses small private helper functions:

- `_is_inside_board(...)` checks whether a neighbour position is valid.
- `_count_mines_around(...)` counts mines around one cell.

This keeps the main function easy to read without changing the required public
function signature.

## Run The Sample

From this folder:

```bash
python3 solution_minesweeper.py
```

Expected result:

```text
OK
```

## Run The Tests

From this folder:

```bash
python3 -m unittest discover -s tests
```

The tests cover:

- The official challenge example.
- Empty boards.
- Boards with no mines.
- Boards with only mines.
- Single-cell boards.
- Rectangular boards.
- Corner and edge neighbour counting.
- Confirming the input board is not modified.
