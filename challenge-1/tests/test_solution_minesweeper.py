import importlib.util
import unittest
from pathlib import Path

SOLUTION_PATH = Path(__file__).resolve().parents[1] / "solution_minesweeper.py"
SPEC = importlib.util.spec_from_file_location("solution_minesweeper", SOLUTION_PATH)
solution_minesweeper = importlib.util.module_from_spec(SPEC)

if SPEC.loader is None:
    raise ImportError(f"Could not load {SOLUTION_PATH}")

SPEC.loader.exec_module(solution_minesweeper)
count_neighbouring_mines = solution_minesweeper.count_neighbouring_mines


class CountNeighbouringMinesTest(unittest.TestCase):
    def test_official_example(self):
        board = [
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

        self.assertEqual(count_neighbouring_mines(board), expected)

    def test_empty_board(self):
        self.assertEqual(count_neighbouring_mines([]), [])

    def test_board_with_empty_row(self):
        self.assertEqual(count_neighbouring_mines([[]]), [[]])

    def test_single_empty_cell(self):
        self.assertEqual(count_neighbouring_mines([[0]]), [[0]])

    def test_single_mine_cell(self):
        self.assertEqual(count_neighbouring_mines([[1]]), [[9]])

    def test_board_with_no_mines(self):
        board = [
            [0, 0, 0],
            [0, 0, 0],
        ]

        expected = [
            [0, 0, 0],
            [0, 0, 0],
        ]

        self.assertEqual(count_neighbouring_mines(board), expected)

    def test_board_with_only_mines(self):
        board = [
            [1, 1],
            [1, 1],
        ]

        expected = [
            [9, 9],
            [9, 9],
        ]

        self.assertEqual(count_neighbouring_mines(board), expected)

    def test_rectangular_board(self):
        board = [
            [1, 0, 0, 1],
            [0, 0, 0, 0],
        ]

        expected = [
            [9, 1, 1, 9],
            [1, 1, 1, 1],
        ]

        self.assertEqual(count_neighbouring_mines(board), expected)

    def test_corner_and_edge_neighbours(self):
        board = [
            [1, 0, 1],
            [0, 0, 0],
            [1, 0, 1],
        ]

        expected = [
            [9, 2, 9],
            [2, 4, 2],
            [9, 2, 9],
        ]

        self.assertEqual(count_neighbouring_mines(board), expected)

    def test_does_not_modify_input_board(self):
        board = [
            [0, 1],
            [0, 0],
        ]
        original = [row[:] for row in board]

        count_neighbouring_mines(board)

        self.assertEqual(board, original)


if __name__ == "__main__":
    unittest.main()
