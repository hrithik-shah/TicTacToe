import pygame, sys
import numpy as np

DIMENSION = 975
SQUARE_SIZE = DIMENSION // 3
BOARD_SHIFT = DIMENSION // 4
LINE_SPACE = int( 20 / 900 * DIMENSION )
LINE_SIZE = int( 12 / 900 * DIMENSION )
CIRCLE_RADIUS = ( DIMENSION * 105 ) // 900
CIRCLE_WIDTH = ( DIMENSION * 14) // 900
CROSS_SIZE = ( SQUARE_SIZE * 19 ) // 300

pygame.init()

screen = pygame.display.set_mode( (int( 1.5*DIMENSION ), DIMENSION) )
pygame.display.set_caption( "Tic Tac Toe" )

#board
board = np.zeros( (3, 3) )

def draw_screen():
    # background
    screen.fill( (60, 60, 60) )
    screen.fill( (45, 45, 45), (0, 0, BOARD_SHIFT, DIMENSION) )
    screen.fill( (45, 45, 45), (BOARD_SHIFT + DIMENSION, 0, 1.5*DIMENSION, DIMENSION) )

    # 1 horizontal
    pygame.draw.line( screen, (0, 128, 128), (LINE_SPACE + BOARD_SHIFT, SQUARE_SIZE), (DIMENSION - LINE_SPACE + BOARD_SHIFT, SQUARE_SIZE), LINE_SIZE )
    # 2 horizontal
    pygame.draw.line( screen, (0, 128, 128), (LINE_SPACE + BOARD_SHIFT, 2*SQUARE_SIZE), (DIMENSION - LINE_SPACE + BOARD_SHIFT, 2*SQUARE_SIZE), LINE_SIZE )

    # 1 vertical
    pygame.draw.line( screen, (0, 128, 128), (SQUARE_SIZE + BOARD_SHIFT, LINE_SPACE), (SQUARE_SIZE + BOARD_SHIFT, DIMENSION - LINE_SPACE), LINE_SIZE )
    # 2 vertical
    pygame.draw.line( screen, (0, 128, 128), (2*SQUARE_SIZE + BOARD_SHIFT, LINE_SPACE), (2*SQUARE_SIZE + BOARD_SHIFT, DIMENSION - LINE_SPACE), LINE_SIZE )

def draw_figures():
    SPACE = ( DIMENSION * 60 ) // 900

    for row in range( 3 ):
        for col in range( 3 ): 

            if board[row][col] == 1:
                #ascending
                pygame.draw.line( screen, (0, 128, 128), (BOARD_SHIFT + col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (BOARD_SHIFT + col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_SIZE )
                #descending
                pygame.draw.line( screen, (0, 128, 128), (BOARD_SHIFT + col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (BOARD_SHIFT + col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_SIZE )

            elif board[row][col] == 2:
                pygame.draw.circle( screen, (0, 128, 128), (BOARD_SHIFT + col * SQUARE_SIZE + SQUARE_SIZE//2, row * SQUARE_SIZE + SQUARE_SIZE//2), CIRCLE_RADIUS, CIRCLE_WIDTH )


def mark_square(rol, col, player):
    board[rol][col] = player

def available_square(row, col):
    if col < 3 and col > -1:
        return board[row][col] == 0

def is_board_full():
    for row in board:
        for value in row:
            if value == 0:
                return False
    return True

def is_board_empty():
    for row in board:
        for value in row:
            if value == 1 or value == 2:
                return False
    return True

def check_win( player ):
    # vertical check
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] == player:
            draw_vertical_winning_line( col, player )
            return True

    # horizontal check
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] == player:
            draw_horizontal_winning_line( row, player )
            return True

    # ascending diagonal check
    if board[0][2] == board[1][1] == board[2][0] == player:
        draw_ascending_diagonal_winning_line( player )
        return True 

    # descending diagonal check
    if board[0][0] == board[1][1] == board[2][2] == player:
        draw_descending_diagonal_winning_line( player )
        return True
    
    return False

def draw_vertical_winning_line( col, player ):
    SPACE = ( DIMENSION * 25 ) // 900
    pygame.draw.line( screen, (0, 128, 128), (BOARD_SHIFT + col * SQUARE_SIZE + SQUARE_SIZE//2, SPACE), (BOARD_SHIFT + col * SQUARE_SIZE + SQUARE_SIZE//2, DIMENSION - SPACE), LINE_SIZE )

def draw_horizontal_winning_line( row, player ):
    SPACE = ( DIMENSION * 25 ) // 900
    pygame.draw.line( screen, (0, 128, 128), (BOARD_SHIFT + SPACE, row * SQUARE_SIZE + SQUARE_SIZE//2), (BOARD_SHIFT + DIMENSION - SPACE, row * SQUARE_SIZE + SQUARE_SIZE//2), LINE_SIZE )

def draw_ascending_diagonal_winning_line( player ):
    SPACE = ( DIMENSION * 25 ) // 900
    pygame.draw.line( screen, (0, 128, 128), (BOARD_SHIFT + SPACE, DIMENSION - SPACE), (BOARD_SHIFT + DIMENSION - SPACE, SPACE), CROSS_SIZE )

def draw_descending_diagonal_winning_line( player ):
    SPACE = ( DIMENSION * 25 ) // 900
    pygame.draw.line( screen, (0, 128, 128), (BOARD_SHIFT + SPACE, SPACE), (BOARD_SHIFT + DIMENSION - SPACE, DIMENSION - SPACE), CROSS_SIZE )

def restart():
    global game_over
    game_over = False
    screen.fill( (60, 60, 60) )
    draw_screen()
    player = 1
    for row in range(3):
        for col in range(3):
            board[row][col] = 0

draw_screen()

player = 1
game_over = False

#mainloop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

            mouseX = event.pos[0]
            mouseY = event.pos[1]

            clicked_row = int( mouseY // SQUARE_SIZE )
            clicked_col = int( (mouseX - BOARD_SHIFT) // SQUARE_SIZE )

            if is_board_empty():
                player = 1

            if available_square( clicked_row, clicked_col):
                mark_square( clicked_row, clicked_col, player )
                game_over = check_win( player )
                player = player % 2 + 1
                
            draw_figures()

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                restart()
                
    pygame.display.update()