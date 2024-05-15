import pygame
import secrets

pygame.init()

# initial set up
WIDTH = 400
HEIGHT = 500
screen = pygame.display.set_mode([WIDTH, HEIGHT])
pygame.display.set_caption('2048')
timer = pygame.time.Clock()
fps = 60
font = pygame.font.Font('freesansbold.ttf', 24)

# 2048 game color library
colors = {0: (204, 192, 179),
          2: (238, 228, 218),
          4: (237, 224, 200),
          8: (242, 177, 121),
          16: (245, 149, 99),
          32: (246, 124, 95),
          64: (246, 94, 59),
          128: (237, 207, 114),
          256: (237, 204, 97),
          512: (237, 200, 80),
          1024: (237, 197, 63),
          2048: (237, 194, 46),
          'light text': (249, 246, 242),
          'dark text': (119, 110, 101),
          'other': (0, 0, 0),
          'bg': (187, 173, 160)}

# game variables initialize
board_values = [[0 for _ in range(4)] for _ in range(4)]
game_over = False
spawn_new = True
init_count = 0
direction = ''
global_score = 0
file = open('high_score', 'r')
init_high = int(file.readline())
file.close()
high_score = init_high


# draw game over and restart text
def draw_over():
    pygame.draw.rect(screen, 'black', [50, 50, 300, 100], 0, 10)
    game_over_text1 = font.render('Game Over!', True, 'white')
    game_over_text2 = font.render('Press Enter to Restart', True, 'white')
    screen.blit(game_over_text1, (130, 65))
    screen.blit(game_over_text2, (70, 105))


def up(board, merged):
    score_up = 0

    for i in range(1, 4):  # Начинаем с индекса 1, так как первая строка не может быть смещена вверх
        for j in range(4):
            score_up += shift_tile_up(board, merged, i, j)

    return score_up


def shift_tile_up(board, merged, i, j):
    score = 0
    shift = 0

    for q in range(i):
        if board[q][j] == 0:
            shift += 1

    if shift > 0:
        board[i - shift][j] = board[i][j]
        board[i][j] = 0

    if board[i - shift - 1][j] == board[i - shift][j] and not merged[i - shift][j] \
            and not merged[i - shift - 1][j]:
        board[i - shift - 1][j] *= 2
        score = board[i - shift - 1][j]
        board[i - shift][j] = 0
        merged[i - shift - 1][j] = True

    return score


def down(board, merged):
    score_down = 0

    for i in range(2, -1, -1):  # Начинаем с индекса 2, так как последняя строка не может быть смещена вниз
        for j in range(4):
            score_down += shift_tile_down(board, merged, i, j)

    return score_down


def shift_tile_down(board, merged, i, j):
    score = 0
    shift = 0

    for q in range(i + 1):
        if board[3 - q][j] == 0:
            shift += 1

    if shift > 0:
        board[2 - i + shift][j] = board[2 - i][j]
        board[2 - i][j] = 0

    if 3 - i + shift <= 3 and board[2 - i + shift][j] == board[3 - i + shift][j] \
            and not merged[3 - i + shift][j] and not merged[2 - i + shift][j]:
        board[3 - i + shift][j] *= 2
        score = board[3 - i + shift][j]
        board[2 - i + shift][j] = 0
        merged[3 - i + shift][j] = True

    return score


def left(board, merged):
    score_left = 0

    for i in range(4):
        for j in range(1, 4):  # Начинаем с индекса 1, так как первый столбец не может быть смещен влево
            score_left += shift_tile_left(board, merged, i, j)

    return score_left


def shift_tile_left(board, merged, i, j):
    score = 0
    shift = 0

    for q in range(j):
        if board[i][q] == 0:
            shift += 1

    if shift > 0:
        board[i][j - shift] = board[i][j]
        board[i][j] = 0

    if board[i][j - shift] == board[i][j - shift - 1] and not merged[i][j - shift - 1] \
            and not merged[i][j - shift]:
        board[i][j - shift - 1] *= 2
        score = board[i][j - shift - 1]
        board[i][j - shift] = 0
        merged[i][j - shift - 1] = True

    return score


def right(board, merged):
    score_right = 0

    for i in range(4):
        for j in range(2, -1, -1):  # Начинаем с индекса 2, так как последний столбец не может быть смещен вправо
            score_right += shift_tile_right(board, merged, i, j)

    return score_right


def shift_tile_right(board, merged, i, j):
    score = 0
    shift = 0

    for q in range(j):
        if board[i][3 - q] == 0:
            shift += 1

    if shift > 0:
        board[i][3 - j + shift] = board[i][3 - j]
        board[i][3 - j] = 0

    if 4 - j + shift <= 3 and board[i][4 - j + shift] == board[i][3 - j + shift] \
            and not merged[i][4 - j + shift] and not merged[i][3 - j + shift]:
        board[i][4 - j + shift] *= 2
        score = board[i][4 - j + shift]
        board[i][3 - j + shift] = 0
        merged[i][4 - j + shift] = True

    return score


# take your turn based on direction
def take_turn(direc, board):
    global global_score
    merged = [[False for _ in range(4)] for _ in range(4)]
    if direc == 'UP':
        global_score += up(board, merged)

    elif direc == 'DOWN':
        global_score += down(board, merged)

    elif direc == 'LEFT':
        global_score += left(board, merged)

    elif direc == 'RIGHT':
        global_score += right(board, merged)
    return board


# spawn in new pieces randomly when turns start
def new_pieces(board):
    count = 0
    full = False
    while any(0 in row for row in board) and count < 1:
        row = secrets.randbelow(4)
        col = secrets.randbelow(4)
        if board[row][col] == 0:
            count += 1
            if secrets.randbelow(10) == 0:
                board[row][col] = 4
            else:
                board[row][col] = 2
    if count < 1:
        full = True
    return board, full


# draw background for the board
def draw_board():
    pygame.draw.rect(screen, colors['bg'], [0, 0, 400, 400], 0, 10)
    score_text = font.render(f'Score: {global_score}', True, 'black')
    high_score_text = font.render(f'High Score: {high_score}', True, 'black')
    screen.blit(score_text, (10, 410))
    screen.blit(high_score_text, (10, 450))


# draw tiles for game
def draw_pieces(board):
    for i in range(4):
        for j in range(4):
            value = board[i][j]
            if value > 8:
                value_color = colors['light text']
            else:
                value_color = colors['dark text']
            if value <= 2048:
                color = colors[value]
            else:
                color = colors['other']
            pygame.draw.rect(screen, color, [j * 95 + 20, i * 95 + 20, 75, 75], 0, 5)
            if value > 0:
                value_len = len(str(value))
                font = pygame.font.Font('freesansbold.ttf', 48 - (5 * value_len))
                value_text = font.render(str(value), True, value_color)
                text_rect = value_text.get_rect(center=(j * 95 + 57, i * 95 + 57))
                screen.blit(value_text, text_rect)
                pygame.draw.rect(screen, 'black', [j * 95 + 20, i * 95 + 20, 75, 75], 2, 5)


# main game loop
run = True
while run:
    timer.tick(fps)
    screen.fill('gray')
    draw_board()
    draw_pieces(board_values)
    if spawn_new or init_count < 2:
        board_values, game_over = new_pieces(board_values)
        spawn_new = False
        init_count += 1
    if direction != '':
        board_values = take_turn(direction, board_values)
        direction = ''
        spawn_new = True
    if game_over:
        draw_over()
        if high_score > init_high:
            file = open('high_score', 'w')
            file.write(f'{high_score}')
            file.close()
            init_high = high_score

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                direction = 'UP'
            elif event.key == pygame.K_DOWN:
                direction = 'DOWN'
            elif event.key == pygame.K_LEFT:
                direction = 'LEFT'
            elif event.key == pygame.K_RIGHT:
                direction = 'RIGHT'

            if game_over and event.key == pygame.K_RETURN:
                    board_values = [[0 for _ in range(4)] for _ in range(4)]
                    spawn_new = True
                    init_count = 0
                    global_score = 0
                    direction = ''
                    game_over = False

    if global_score > high_score:
        high_score = global_score

    pygame.display.flip()
pygame.quit()
