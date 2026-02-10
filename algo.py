import copy

EMPTY = "."
BOARD_SIZE = 9
BOX_SIZE = 3


def get_box_index(i: int, j: int) -> int:
    """
    Get the index of the box that the cell (i, j) belongs to.
    """
    return BOX_SIZE * (i // BOX_SIZE) + (j // BOX_SIZE)


def solve_sudoku(board: list[list[str]]) -> list[list[str]]:
    """
    Solve a Sudoku puzzle.

    Args:
        board: A 9x9 list of lists of strings, where each string is a digit or EMPTY

    Returns:
        A list of lists of strings, where each string is a digit or EMPTY
    """

    # Validate board
    if len(board) != BOARD_SIZE or any(len(row) != BOARD_SIZE for row in board):
        raise ValueError("The Sudoku board must be 9x9.")

    # Initialize
    solutions = []
    filled_rows = [set() for _ in range(BOARD_SIZE)]
    filled_cols = [set() for _ in range(BOARD_SIZE)]
    filled_boxes = [set() for _ in range(BOARD_SIZE)]
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            value = board[i][j]
            if value != EMPTY:
                filled_rows[i].add(value)
                filled_cols[j].add(value)
                filled_boxes[get_box_index(i, j)].add(value)

    def backtrack(row: int, col: int) -> None:
        if row == BOARD_SIZE:
            solutions.append(copy.deepcopy(board))
            return

        # Skip if cell is already filled
        if board[row][col] != EMPTY:
            if col == BOARD_SIZE - 1:
                backtrack(row + 1, 0)
            else:
                backtrack(row, col + 1)
            return

        for k in ["1", "2", "3", "4", "5", "6", "7", "8", "9"]:

            # 1. Skip if not feasible
            if (
                k in filled_rows[row]
                or k in filled_cols[col]
                or k in filled_boxes[get_box_index(row, col)]
            ):
                continue

            # 2. Update board + constraints
            board[row][col] = k
            filled_rows[row].add(k)
            filled_cols[col].add(k)
            filled_boxes[get_box_index(row, col)].add(k)

            # 3. Backtrack
            if col == BOARD_SIZE - 1:
                backtrack(row + 1, 0)
            else:
                backtrack(row, col + 1)

            # 4. Undo update board + undo constraints
            board[row][col] = EMPTY
            filled_rows[row].remove(k)
            filled_cols[col].remove(k)
            filled_boxes[get_box_index(row, col)].remove(k)

    backtrack(0, 0)
    return solutions
