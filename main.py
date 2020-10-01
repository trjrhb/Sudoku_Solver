#
""" Sudoku Solver

What is Sudoku?
A puzzle in which players insert the numbers one to nine into a grid consisting of nine squares subdivided into a
further nine smaller squares in such a way that every number appears once in each horizontal line, vertical line,
and square.

Goal: To implement a backtracking algorithm that can recursively solve a sudoku puzzle

"""
from Sudoku.Sudoku import Sudoku
import random

if __name__ == "__main__":
    random.seed()

    puzzle = Sudoku()

    print("Starting Puzzle")
    print(puzzle)

    if puzzle.solve_puzzle():
        print ("Solution Found!")
        print(puzzle)
    else:
        print("No solution found...")
1