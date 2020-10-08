from Constants import *
import pygame
import random


class Grid:
    def __init__(self, difficulty):
        self.difficulty = difficulty

        self.puzzle = [[Box(x * SQUARE_PX_SIZE, y * SQUARE_PX_SIZE) for x in range(MAX_INDEX)] for y in
                       range(MAX_INDEX)]
        self.generate_new_puzzle()
        self.delete_clues()

        self.strikes = 0
        self.multiplier = 1
        self.score = 0

    # Draws all the lines and boxes to create a Sudoku grid
    def draw_grid(self, win):

        pygame.draw.rect(win, BLACK, (WIDTH - 5, 0, 5, WIDTH))  # Thick Right Line
        pygame.draw.rect(win, BLACK, (0, WIDTH, WIDTH, 5))  # Thick Bottom Line

        for row in range(MAX_INDEX):
            if row % 3 == 0:
                pygame.draw.rect(win, BLACK, (0, row * SQUARE_PX_SIZE, WIDTH, 5))

            for col in range(MAX_INDEX):
                if col % 3 == 0:
                    pygame.draw.rect(win, BLACK, (col * SQUARE_PX_SIZE, 0, 5, WIDTH))

                self.puzzle[row][col].draw_box(win)

    # Displays game stats at the bottom of the window
    def game_stats(self, win):
        font = pygame.font.SysFont(FONT, STATISTICS_FONT_SIZE)

        # Using pygame's font.render to create a surface to layer on top of the window
        multi_text = font.render("Multiplier: " + str(self.multiplier) + "x", 1, BLACK)
        score_text = font.render("Score: " + str(self.score), 1, BLACK)
        strikes_text = font.render("Strikes: " + str(self.strikes), 1, BLACK)
        solve_text = font.render("Solve", 1, BLACK)
        new_puzzle_text = font.render("New Puzzle", 1, BLACK)

        # Updates the statistics shown at the bottom of the window
        win.blit(multi_text, (50, 945))
        win.blit(score_text, (50, 1020))
        win.blit(strikes_text, (50, 1095))

        win.blit(solve_text, (620, 1020))
        win.blit(new_puzzle_text, (520, 1095))

    # Decrements the multiplier as a result of the player not placing a piece in a certain amount of time
    def dec_multiplier(self):
        if self.multiplier > 2:
            self.multiplier -= MULT_PER_BLOCK
        else:
            self.multiplier = 1

    # Determines the location that the player is trying to place a number
    def determine_selection(self, mouse, selection):
        row_index = mouse[1] // SQUARE_PX_SIZE
        col_index = mouse[0] // SQUARE_PX_SIZE
        self.puzzle[selection[0]][selection[1]].selected = False

        # Handles if the player clicks somewhere besides the 9x9 puzzle
        if row_index >= MAX_INDEX or col_index >= MAX_INDEX:
            return [-1, -1]

        self.puzzle[row_index][col_index].selected = True
        return [row_index, col_index]

    # Places the number in the selected box if it an acceptable placement
    def update_value(self, selection, value):
        row = selection[0]
        col = selection[1]

        # Start multiplier dec timer and every 20 seconds it calls dec_multiplier()
        pygame.time.set_timer(pygame.USEREVENT, 20000)

        # Validates that the same value isn't in the same row, column or 3x3 box
        if self.safe_placement(value, row, col):
            self.puzzle[row][col].set_value(value)

            self.score += int(SCORE_PER_BLOCK * self.multiplier)
            self.multiplier += MULT_PER_BLOCK
        else:
            # Increments the number of failed placements if it is not acceptable to place
            self.strikes += 1

    # Creates a new puzzle for the user
    def generate_new_puzzle(self):
        num_seeds = 0  # The amount of randomly placed numbers that "seeds" the puzzle

        while num_seeds <= SEEDS:
            row = random.randint(MIN_INDEX, MAX_INDEX - 1)
            col = random.randint(MIN_INDEX, MAX_INDEX - 1)
            rand_num = random.randint(SMALLEST_NUM, LARGEST_NUM - 1)

            if self.puzzle[row][col].get_value() == EMPTY_SPACE and self.safe_placement(rand_num, row, col):
                self.puzzle[row][col].set_value(rand_num)
                num_seeds += 1

        # Fills any blank spaces using the backtracking algorithm to prevent an puzzles from being unsolvable
        if self.solve_puzzle():
            return True

    # Uses a backtracking algorithm that finds a solution to the puzzle
    def solve_puzzle(self):
        row, col = self.find_empty_space()

        # If all spaces have been assigned and validated then program has finished
        if row == DEFAULT_LOCATION and col == DEFAULT_LOCATION:
            return True

        for num in range(SMALLEST_NUM, LARGEST_NUM):  # (Range 1-9)
            # If the num doesn't exist in the row, column, or current box then assign it to that position
            if self.safe_placement(num, row, col):

                # Assign num to current location
                self.puzzle[row][col].set_value(num)

                # Recursively call backtracking algo
                if self.solve_puzzle():
                    return True

                # Since the recursive solution was incorrect set it to an empty space
                self.puzzle[row][col].set_value(EMPTY_SPACE)

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
            if self.puzzle[row][col].get_value() == num:
                return True

        return False

    # Validates that num doesn't exist in the same column we are trying to assign the a value to
    def adopted_in_col(self, num, col):
        for row in range(MIN_INDEX, MAX_INDEX):
            if self.puzzle[row][col].get_value() == num:
                return True

        return False

    # Validates that num doesn't exist in the same box (3x3 area) we are trying to assign the a value to
    def adopted_in_box(self, num, row, col):
        # Indicates which 3x3 box it should check and starts in the top left corner
        box_row_start = (row / NUM_BOXES) * NUM_SQUARES
        box_col_start = (col / NUM_BOXES) * NUM_SQUARES

        for rows in range(MIN_INDEX, NUM_BOXES):
            for columns in range(MIN_INDEX, NUM_BOXES):
                if self.puzzle[rows + box_row_start][columns + box_col_start].get_value() == num:
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
                if self.puzzle[row][col].get_value() == EMPTY_SPACE:
                    empty_row = row
                    empty_col = col
                    break

        return empty_row, empty_col

    # Returns True if the box has not been assigned a value other than 0
    def is_empty(self, selected_box):
        row = selected_box[0]
        col = selected_box[1]
        if self.puzzle[row][col].get_value() == EMPTY_SPACE:
            return True
        return False

    # Utility method that displays the current state of the sudoku puzzle (Mostly for debugging)
    def __repr__(self):
        for row in range(MAX_INDEX):
            for col in range(MAX_INDEX):
                print(self.puzzle[row][col].get_value()),
            print('')
        return '\n'

    # Has a chance to replace a clue with an empty space
    def delete_clues(self):
        # The amount of deleted clues is determined by the difficulty level
        for row in range(MAX_INDEX):
            for col in range(MAX_INDEX):
                rand_num = random.randint(1, 100)
                if rand_num <= self.difficulty:
                    self.puzzle[row][col].set_value(EMPTY_SPACE)


class Box:
    PADDING = 25

    def __init__(self, x, y, val=0):
        self.value = val
        self.x_coord = x
        self.y_coord = y
        self.selected = False

    def __repr__(self):
        return str(self.value)

    def draw_box(self, win):
        font = pygame.font.SysFont(FONT, FONT_SIZE)

        # A check to make sure we don't show any zeros on the screen
        if self.value == EMPTY_SPACE:
            text = font.render("", 1, BLACK)
        else:
            text = font.render(str(self.value), 1, BLACK)

        # Makes the box the user has selected a different color for easier viewing
        if self.selected:
            pygame.draw.rect(win, RED, (self.x_coord, self.y_coord, SQUARE_PX_SIZE, SQUARE_PX_SIZE), 5)
        else:
            pygame.draw.rect(win, BLACK, (self.x_coord, self.y_coord, SQUARE_PX_SIZE, SQUARE_PX_SIZE), 1)
        win.blit(text, (self.x_coord + self.PADDING, self.y_coord))

    def set_value(self, val):
        self.value = val

    def get_value(self):
        return self.value

    def get_coord(self):
        return [self.x_coord, self.y_coord]
