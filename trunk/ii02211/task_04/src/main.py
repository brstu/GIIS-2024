import pygame
import random
import time

# Инициализация Pygame
pygame.init()

# Цвета
WHITE = (255, 255, 255)
RED = (213, 50, 80)
GREEN = (0, 255, 0)
BLUE = (50, 153, 213)

# Размеры экрана
WIDTH, HEIGHT = 600, 400

# Размер ячейки игрового поля
CELL_SIZE = 20

# Скорость змейки (по умолчанию)
SPEED = 10

# Создание игрового окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Пожиратель красных квадратиков")

# Класс для змейки
class Snake:
    def __init__(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = GREEN

    # Метод для движения змейки
    def move(self):
        cur = self.positions[0]
        x, y = self.direction
        new = (((cur[0] + (x * CELL_SIZE)) % WIDTH), (cur[1] + (y * CELL_SIZE)) % HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()

    # Метод для смены направления движения змейки
    def change_direction(self, direction):
        if direction[0] * -1 != self.direction[0] and direction[1] * -1 != self.direction[1]:
            self.direction = direction

    # Метод для увеличения длины змейки
    def increase_length(self):
        self.length += 1

    # Метод для сброса позиции змейки
    def reset(self):
        self.length = 1
        self.positions = [((WIDTH / 2), (HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])

    # Метод для отрисовки змейки
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, WHITE, r, 1)

# Класс для еды
class Food:
    def __init__(self):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position()

    # Метод для случайной установки позиции еды
    def randomize_position(self):
        self.position = (random.randint(0, WIDTH - CELL_SIZE) // CELL_SIZE * CELL_SIZE,
                         random.randint(0, HEIGHT - CELL_SIZE) // CELL_SIZE * CELL_SIZE)

    # Метод для отрисовки еды
    def draw(self, surface):
        r = pygame.Rect((self.position[0], self.position[1]), (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, WHITE, r, 1)

# Направления
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Основная функция игры
def main():
    global SPEED
    snake = Snake()
    food = Food()

    clock = pygame.time.Clock()

    score = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    snake.change_direction(UP)
                elif event.key == pygame.K_DOWN:
                    snake.change_direction(DOWN)
                elif event.key == pygame.K_LEFT:
                    snake.change_direction(LEFT)
                elif event.key == pygame.K_RIGHT:
                    snake.change_direction(RIGHT)
                elif event.key == pygame.K_SPACE:
                    snake.increase_length()
                elif event.key == pygame.K_s:
                    SPEED += 2
                elif event.key == pygame.K_d:
                    if SPEED > 2:
                        SPEED -= 2

        snake.move()
        if snake.positions[0] == food.position:
            snake.increase_length()
            food.randomize_position()
            score += 1

        screen.fill(BLUE)
        snake.draw(screen)
        food.draw(screen)
        
        # Отображение счета
        font = pygame.font.SysFont(None, 30)
        text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))

        pygame.display.update()
        clock.tick(SPEED)

if __name__ == "__main__":
    main()
