# Импорт модулей
import pygame
import random

# Инициализация Pygame
pygame.init()

# Параметры экрана
WIDTH, HEIGHT = 300, 600
BLOCK_SIZE = 30
GRID_WIDTH, GRID_HEIGHT = WIDTH // BLOCK_SIZE, HEIGHT // BLOCK_SIZE

# Цвета
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)

# Фигуры тетриса
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]  # Z
]

# Инициализация окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tetris")

# Функция отрисовки сетки
def draw_grid(surface):
    for x in range(0, WIDTH, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, BLOCK_SIZE):
        pygame.draw.line(surface, GRAY, (0, y), (WIDTH, y))


# Функция отрисовки блока
def draw_block(surface, color, x, y):
    pygame.draw.rect(surface, color, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


# Функция проверки возможности движения фигуры
def can_move(board, shape, x, y):
    for dy in range(len(shape)):
        for dx in range(len(shape[0])):
            if shape[dy][dx] and (x + dx < 0 or x + dx >= GRID_WIDTH or y + dy >= GRID_HEIGHT or board[y + dy][x + dx]):
                return False
    return True


# Функция поворота фигуры
def rotate(shape):
    return [[shape[y][x] for y in range(len(shape))] for x in range(len(shape[0]) - 1, -1, -1)]


# Функция создания новой фигуры
def new_piece():
    shape = random.choice(SHAPES)
    x = GRID_WIDTH // 2 - len(shape[0]) // 2
    y = 0
    return shape, x, y


# Функция обновления доски
def update_board(board, shape, x, y):
    for dy in range(len(shape)):
        for dx in range(len(shape[0])):
            if shape[dy][dx]:
                board[y + dy][x + dx] = 1


# Функция проверки заполненных линий
def check_lines(board):
    lines_cleared = 0
    for i in range(GRID_HEIGHT):
        if all(board[i]):
            del board[i]
            board.insert(0, [0] * GRID_WIDTH)
            lines_cleared += 1
    return lines_cleared


# Функция отрисовки кнопки "Start"
def draw_start_button(surface, game_over):
    start_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT // 10)
    pygame.draw.rect(surface, RED, start_button_rect)
    start_font = pygame.font.Font(None, 50)
    start_text = start_font.render("Start", True, WHITE)
    surface.blit(start_text, (start_button_rect.x + start_button_rect.width // 2 - start_text.get_width() // 2,
                              start_button_rect.y + start_button_rect.height // 2 - start_text.get_height() // 2))


# Функция отрисовки поля для ввода имени
def draw_name_input(surface, name_input, active):
    input_box = pygame.Rect(10, 10, 280, 40)
    name_input = 'name'
    color_inactive = pygame.Color('lightskyblue3')
    color_active = pygame.Color('dodgerblue2')
    color = color_active if active else color_inactive
    pygame.draw.rect(surface, color, input_box, 2)
    font = pygame.font.Font(None, 32)
    text_surface = font.render(name_input, True, color)
    surface.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    if input_box == '':
        input_box = 'Name'
    # else:
    #     input_box = name_input
    return input_box


# Функция отрисовки кнопки "Record"
def draw_record_button(surface, game_over):
    record_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, HEIGHT // 10)
    pygame.draw.rect(surface, RED, record_button_rect)
    record_font = pygame.font.Font(None, 50)
    record_text = record_font.render("Record", True, WHITE)
    surface.blit(record_text, (record_button_rect.x + record_button_rect.width // 2 - record_text.get_width() // 2,
                               record_button_rect.y + record_button_rect.height // 2 - record_text.get_height() // 2))


# Функция отрисовки счета
def draw_score(surface, score):
    font = pygame.font.Font(None, 30)
    text = font.render("Score: " + str(score), True, WHITE)
    surface.blit(text, (10, 50))  # Изменено положение отображения счета


def write_record(name, score):
    try:
        # Открытие файла на чтение
        with open("records.txt", "r") as file:
            lines = file.readlines()
    except FileNotFoundError:
        # Создание файла, если его не существует
        with open("records.txt", "w") as file:
            file.write(f"{name}: {score}\n")
        return

    # Добавление новой записи и сортировка по убыванию очков
    lines.append(f"{name}: {score}\n")
    lines.sort(key=lambda x: int(x.split(": ")[1]), reverse=True)

    # Запись отсортированного списка в файл
    with open("records.txt", "w") as file:
        file.writelines(lines)


# Основная функция игры
def main():
    clock = pygame.time.Clock()
    board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
    current_shape, x, y = new_piece()
    score = 0
    name = ''
    active = False

    # Переменные для отслеживания времени автоматического падения блоков
    last_move_time = pygame.time.get_ticks()  # Время последнего перемещения блока
    move_interval = 500  # Интервал времени в миллисекундах (0.5 секунды)

    # Создаем переменную input_box за пределами цикла while
    input_box = pygame.Rect(10, 10, 280, 40)
    game_active = 1
    running = True
    game_over = True
    while running:
        screen.fill(BLACK)
        draw_grid(screen)

        current_time = pygame.time.get_ticks()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game_over:
                    start_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2, WIDTH // 2, HEIGHT // 10)
                    record_button_rect = pygame.Rect(WIDTH // 4, HEIGHT // 2 + 100, WIDTH // 2, HEIGHT // 10)
                    if input_box.collidepoint(event.pos):  # Проверяем клик внутри поля ввода
                        active = not active  # Переключение состояния активности поля ввода
                    if start_button_rect.collidepoint(event.pos):
                        game_over = False
                        game_active = 0
                        board = [[0] * GRID_WIDTH for _ in range(GRID_HEIGHT)]
                        current_shape, x, y = new_piece()
                        score = 0
                        active = True  # Показываем поле ввода имени при нажатии "Старт"
                    elif record_button_rect.collidepoint(event.pos):
                        if game_active == 0:
                            write_record(name, score)
                            game_active = 1
            elif event.type == pygame.KEYDOWN:
                if not game_over:
                    if event.key == pygame.K_LEFT:
                        if can_move(board, current_shape, x - 1, y):
                            x -= 1
                    elif event.key == pygame.K_RIGHT:
                        if can_move(board, current_shape, x + 1, y):
                            x += 1
                    elif event.key == pygame.K_DOWN:
                        if can_move(board, current_shape, x, y + 1):
                            y += 1
                    elif event.key == pygame.K_UP:
                        rotated_shape = rotate(current_shape)
                        if can_move(board, rotated_shape, x, y):
                            current_shape = rotated_shape
                    elif event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            # Опускание фигуры моментально вниз
                            while can_move(board, current_shape, x, y + 1):
                                y += 1

        if game_over:
            # Отображение кнопок и поля для ввода имени
            draw_start_button(screen, game_over)
            draw_record_button(screen, game_over)
            input_box = draw_name_input(screen, name, active)  # Обновляем поле ввода и сохраняем его состояние
        else:
            keys = pygame.key.get_pressed()

            # Логика управления блоком с клавиатуры

            # Проверка времени для автоматического падения блока
            if current_time - last_move_time > move_interval:
                if can_move(board, current_shape, x, y + 1):
                    y += 1
                else:
                    update_board(board, current_shape, x, y)
                    lines_cleared = check_lines(board)
                    score += lines_cleared
                    current_shape, x, y = new_piece()
                    if not can_move(board, current_shape, x, y):
                        game_over = True  # Игра окончена
                last_move_time = current_time

            # Отрисовка блока на поле
            for dy in range(len(current_shape)):
                for dx in range(len(current_shape[0])):
                    if current_shape[dy][dx]:
                        draw_block(screen, WHITE, x + dx, y + dy)

            # Отрисовка закрепленных блоков на доске
            for row_idx, row in enumerate(board):
                for col_idx, val in enumerate(row):
                    if val:
                        draw_block(screen, WHITE, col_idx, row_idx)

        # Отображение счета
        draw_score(screen, score)

        pygame.display.flip()
        clock.tick(10)  # Установка частоты обновления экрана

    pygame.quit()


if __name__ == "__main__":
    main()
