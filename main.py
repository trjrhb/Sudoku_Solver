#
""" Sudoku Solver

What is Sudoku?
A puzzle in which players insert the numbers one to nine into a grid consisting of nine squares subdivided into a
further nine smaller squares in such a way that every number appears once in each horizontal line, vertical line,
and square.

Goal: To implement a backtracking algorithm that can recursively solve a sudoku puzzle

"""
from Sudoku.Constants import *
import random
import pygame
from Sudoku.board import Grid


def button(window, x, y, width, height, reg_color, hover_color, fill_size=0, event=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if x < mouse[0] < x + width and y < mouse[1] < y + height:
        pygame.draw.rect(window, hover_color, (x, y, width, height), fill_size)

        if click[0] == 1 and event is not None:
            pygame.event.post(event)

    else:
        pygame.draw.rect(window, reg_color, (x, y, width, height), fill_size)


def main_loop():
    window = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Sudoku')
    run = True
    key = None
    clock = pygame.time.Clock()
    selection = [0, 0]
    sudoku = Grid(EASY_DIFFICULTY)
    while run:

        clock.tick(FPS)
        window.fill(WHITE)
        sudoku.draw_grid(window)
        sudoku.game_stats(window)
        mouse = pygame.mouse.get_pos()

        solve_puzzle_event = pygame.USEREVENT + 1
        solve_puzzle = pygame.event.Event(solve_puzzle_event)
        generate_new_puzzle_event = pygame.USEREVENT + 2
        generate_new_puzzle = pygame.event.Event(generate_new_puzzle_event)

        button(window, 610, 1020, 185, 70, WHITE, BLACK, 1, solve_puzzle)  # Solve Button
        button(window, 515, 1095, 350, 70, WHITE, BLACK, 1, generate_new_puzzle)  # New Puzzle Button

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                selection = sudoku.determine_selection(mouse, selection)
                print(selection)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
            if event.type == pygame.USEREVENT:
                sudoku.dec_multiplier()

            if event.type == solve_puzzle_event:
                sudoku.auto_solve = True
                sudoku.solve_puzzle()

            if event.type == generate_new_puzzle_event:
                sudoku.__init__(EASY_DIFFICULTY)

        if sudoku.is_empty(selection) and key is not None:
            sudoku.update_value(selection, key)
            key = None

        # Prints GAME OVER to the screen
        if sudoku.strikes >= 3:
            font = pygame.font.SysFont(FONT, GAME_OVER_FONT_SIZE)
            game_over_text = font.render("GAME OVER", 1, RED)
            pygame.draw.rect(window, BLACK, (0, HEIGHT * 0.25, WIDTH, 150))
            window.blit(game_over_text, (50, HEIGHT * 0.25))

        pygame.display.update()
    pygame.quit()


pygame.init()
random.seed()
main_loop()
