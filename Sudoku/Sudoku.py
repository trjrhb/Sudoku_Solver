from Constants import *
import random


class Sudoku:
    puzzle = []
    difficulty = 1

    def __init__(self):
        # elf.puzzle = p
        self.puzzle = [[EMPTY_SPACE for x in range(MAX_INDEX)] for y in range(MAX_INDEX)]
        self.generate_new_puzzle()
        self.delete_clues()

    def solve_puzzle(self):
        row, col = self.find_empty_space()

        # If all spaces have been assigned and validated then program has finished
        if row == DEFAULT_LOCATION and col == DEFAULT_LOCATION:
            return True

        for num in range(SMALLEST_NUM, LARGEST_NUM):  # (Range 1-9)
            # If the num doesn't exist in the row, column, or current box then assign it to that position
            if self.safe_placement(num, row, col):

                # Assign num to current location
                self.puzzle[row][col] = num

                # Recursively call backtracking algo
                if self.solve_puzzle():
                    return True

                # Since the recursive solution was incorrect set it to an empty space
                self.puzzle[row][col] = EMPTY_SPACE

        return False

    # Helper method that checks to see if num is acceptable to place
    def safe_placement(self, num, row, col):
        if not self.adopted_in_row(num, row) and not self.adopted_in_col(num, col) \
                and not self.adopted_in_box(num, row, col):
            return True
        return False

    # Validates that num doesn't exist in the same row we are trying to assign the a value to
    def adopted_in_row(self, num, row):
        for col in range(MIN_INDEX, MAX_INDEX):
            if self.puzzle[row][col] == num:
                return True

        return False

    # Validates that num doesn't exist in the same column we are trying to assign the a value to
    def adopted_in_col(self, num, col):
        for row in range(MIN_INDEX, MAX_INDEX):
            if self.puzzle[row][col] == num:
                return True

        return False

    # Validates that num doesn't exist in the same box (3x3 area) we are trying to assign the a value to
    def adopted_in_box(self, num, row, col):
        # Indicates which 3x3 box it should check and starts in the top left corner
        box_row_start = (row / NUM_BOXES) * NUM_SQUARES
        box_col_start = (col / NUM_BOXES) * NUM_SQUARES

        for rows in range(MIN_INDEX, NUM_BOXES):
            for columns in range(MIN_INDEX, NUM_BOXES):
                if self.puzzle[rows + box_row_start][columns + box_col_start] == num:
                    if rows != row and columns != col:  # skips index we are trying to assign a number to
                        return True

        return False

    # Utility function that finds the next empty space within the puzzle and returns its location
    def find_empty_space(self):
        # Using -1 as a default value to determine if there are any empty spaces or not
        empty_row = DEFAULT_LOCATION
        empty_col = DEFAULT_LOCATION
        for row in range(MIN_INDEX, MAX_INDEX):
            for col in range(MIN_INDEX, MAX_INDEX):
                if self.puzzle[row][col] == EMPTY_SPACE:
                    empty_row = row
                    empty_col = col
                    break

        return empty_row, empty_col

    # Utility method that displays the current state of the sudoku puzzle
    def __repr__(self):
        for row in range(MAX_INDEX):
            for col in range(MAX_INDEX):
                print(self.puzzle[row][col]),
            print('')
        return '\n'

    # Creates a new puzzle for the user to solve
    def generate_new_puzzle(self):
        num_seeds = 0  # The amount of randomly placed numbers that "seeds" the puzzle

        while num_seeds <= SEEDS:
            row = random.randint(MIN_INDEX, MAX_INDEX - 1)
            col = random.randint(MIN_INDEX, MAX_INDEX - 1)
            rand_num = random.randint(SMALLEST_NUM, LARGEST_NUM - 1)

            if self.puzzle[row][col] == 0 and self.safe_placement(rand_num, row, col):
                self.puzzle[row][col] = rand_num
                num_seeds += 1

        # Fills any blank spaces using the backtracking algorithm to prevent an puzzles from being unsolvable
        if self.solve_puzzle():
            return True

    # Has a chance to replace a clue with an empty space
    def delete_clues(self):
        # The amount of deleted clues is determined by the difficulty level
        skill_level = 0
        if self.difficulty == 1:
            skill_level = EASY_DIFFICULTY       # 40% chance to replace an index with an empty space
        elif self.difficulty == 2:
            skill_level = MEDIUM_DIFFICULTY     # 45% chance
        if self.difficulty == 3:
            skill_level = HARD_DIFFICULTY       # 50% chance
        if self.difficulty == 4:
            skill_level = INSANE_DIFFICULTY     # 60% chance

        for row in range(MAX_INDEX):
            for col in range(MAX_INDEX):
                rand_num = random.randint(1, 100)
                if rand_num <= skill_level:
                    self.puzzle[row][col] = EMPTY_SPACE
