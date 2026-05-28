# Minesweeper: Number of Neighbouring Mines
# Language: Python 3.12

MINE = 1
MINE_IN_OUTPUT = 9

# A cell has up to eight neighbours. Each pair means:
# (change in row, change in column)
NEIGHBOUR_DIRECTIONS = (
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
)


def _is_inside_board(row: int, col: int, total_rows: int, total_cols: int) -> bool:
    """Return True when row and col point to a valid board position."""
    return 0 <= row < total_rows and 0 <= col < total_cols


def _count_mines_around(board: list, row: int, col: int) -> int:
    """Count how many neighbouring cells around board[row][col] contain mines."""
    total_rows = len(board)
    total_cols = len(board[0])
    mines = 0

    for row_delta, col_delta in NEIGHBOUR_DIRECTIONS:
        neighbour_row = row + row_delta
        neighbour_col = col + col_delta

        if not _is_inside_board(
            neighbour_row,
            neighbour_col,
            total_rows,
            total_cols,
        ):
            continue

        if board[neighbour_row][neighbour_col] == MINE:
            mines += 1

    return mines


def count_neighbouring_mines(board: list) -> list:
    """
    Counts neighbouring mines for each cell in a Minesweeper board.

    Parameters:
        board (list): A 2D list where 0 represents an empty space
                      and 1 represents a mine

    Returns:
        list: A 2D list where each cell contains the count of neighbouring mines,
              or 9 if the cell contains a mine
    """
    # Empty boards have no cells to inspect. Return a copy so the function
    # still behaves like it creates a new board.
    if not board or not board[0]:
        return [row[:] for row in board]

    rows = len(board)
    cols = len(board[0])

    # Start with a board full of zeroes, then fill each position with either
    # 9 for a mine or the number of mines found around that position.
    result = [[0] * cols for _ in range(rows)]

    for row in range(rows):
        for col in range(cols):
            if board[row][col] == MINE:
                result[row][col] = MINE_IN_OUTPUT
                continue

            result[row][col] = _count_mines_around(board, row, col)

    return result


if __name__ == "__main__":
    sample_input = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 1],
        [1, 1, 0, 0],
    ]
    expected = [
        [1, 9, 2, 1],
        [2, 3, 9, 2],
        [3, 9, 4, 9],
        [9, 9, 3, 1],
    ]
    output = count_neighbouring_mines(sample_input)
    assert output == expected, f"Mismatch:\n got: {output}\n expected: {expected}"
    print("OK")
