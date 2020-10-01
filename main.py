#
""" Sudoku Solver

What is Sudoku?
A puzzle in which players insert the numbers one to nine into a grid consisting of nine squares subdivided into a
further nine smaller squares in such a way that every number appears once in each horizontal line, vertical line,
and square.

Goal: To implement a backtracking algorithm that can recursively solve a sudoku puzzle

"""

MAX_INDEX = 9
MIN_INDEX = 0
NUM_SQUARES = 3
NUM_BOXES = 3
EMPTY_SPACE = 0
SMALLEST_NUM = 1
LARGEST_NUM = 10
DEFAULT_LOCATION = -1


def backtrack_algo(puzzle):
    empty_space = find_empty_space(puzzle)

    row = empty_space["row"]
    col = empty_space["col"]

    # If all spaces have been assigned and validated then program has finished
    if row == DEFAULT_LOCATION and col == DEFAULT_LOCATION:
        return True

    for num in range(SMALLEST_NUM, LARGEST_NUM):  # (Range 1-9)
        # If the num doesn't exist in the row, column, or current box then assign it to that position
        if not adopted_in_row(puzzle, num, row) and not adopted_in_col(puzzle, num, col) \
                and not adopted_in_box(puzzle, num, row, col):

            # Assign num to current location
            puzzle[row][col] = num

            # Recursively call backtracking algo
            if backtrack_algo(puzzle):
                return True

            # Since the recursive solution was incorrect set it to an empty space
            puzzle[row][col] = EMPTY_SPACE

    return False


# Validates that num doesn't exist in the same row we are trying to assign the a value to
def adopted_in_row(puzzle, num, row):
    for col in range(MIN_INDEX, MAX_INDEX):
        if puzzle[row][col] == num:
            return True

    return False


# Validates that num doesn't exist in the same column we are trying to assign the a value to
def adopted_in_col(puzzle, num, col):
    for row in range(MIN_INDEX, MAX_INDEX):
        if puzzle[row][col] == num:
            return True

    return False


# Validates that num doesn't exist in the same box (3x3 area) we are trying to assign the a value to
def adopted_in_box(puzzle, num, row, col):
    # Indicates which 3x3 box it should check and starts in the top left corner
    box_row_start = (row / NUM_BOXES) * NUM_SQUARES
    box_col_start = (col / NUM_BOXES) * NUM_SQUARES

    for rows in range(MIN_INDEX, NUM_BOXES):
        for columns in range(MIN_INDEX, NUM_BOXES):
            if puzzle[rows + box_row_start][columns + box_col_start] == num:
                if rows != row and columns != col:  # skips index we are trying to assign a number to
                    return True

    return False


# Utility function that finds the next empty space within the puzzle and returns its location
def find_empty_space(puzzle):
    # Using -1 as a default value to determine if there are any empty spaces or not
    location = {"row": DEFAULT_LOCATION, "col": DEFAULT_LOCATION}
    for row in range(MIN_INDEX, MAX_INDEX):
        for col in range(MIN_INDEX, MAX_INDEX):
            if puzzle[row][col] == EMPTY_SPACE:
                location["row"] = row
                location["col"] = col
                break

    return location


# Utility function that displays the current state of the sudoku puzzle
def print_puzzle(puzzle):
    for row in range(MAX_INDEX):
        for col in range(MAX_INDEX):
            print(puzzle[row][col]),
        print('')
    print('\n')


if __name__ == "__main__":

    sudoku = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
              [5, 2, 0, 0, 0, 0, 0, 0, 0],
              [0, 8, 7, 0, 0, 0, 0, 3, 1],
              [0, 0, 3, 0, 1, 0, 0, 8, 0],
              [9, 0, 0, 8, 6, 3, 0, 0, 5],
              [0, 5, 0, 0, 9, 0, 6, 0, 0],
              [1, 3, 0, 0, 0, 0, 2, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 7, 4],
              [0, 0, 5, 2, 0, 6, 3, 0, 0]]

    print("Starting Puzzle")
    print_puzzle(sudoku)

    if backtrack_algo(sudoku):
        print ("Solution Found!")
    else:
        print("No solution found...")
    print_puzzle(sudoku)
