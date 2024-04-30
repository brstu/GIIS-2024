import pygame
from pygame.locals import K_SPACE
from pygame.locals import K_LEFT
from pygame.locals import K_RIGHT
from pygame import mixer
import pickle
from os import path

pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

clock = pygame.time.Clock()
fps = 60

screen_width = 1000
screen_height = 1000

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Определение шрифта
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Определение игровых переменных
tile_size = 50
game_over = 0
main_menu = True
level = 3
max_levels = 7
score = 0

# Определение цвета
white = (255, 255, 255)
blue = (0, 0, 255)

# Загрузка изображения
sun_img = pygame.image.load("../images/sun.png")
bg_img = pygame.image.load("../images/sky.png")
restart_img = pygame.image.load("../images/restart_btn.png")
start_img = pygame.image.load("../images/start_btn.png")
exit_img = pygame.image.load("../images/exit_btn.png")

# Загрузка звуков
pygame.mixer.music.load("../images/music.wav")
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound("../images/coin.wav")
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound("../images/jump.wav")
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound("../images/game_over.wav")
game_over_fx.set_volume(0.5)


def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))


# Функция сброса уровня
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    # Загрузка данных уровня и создание мира
    if path.exists(f"../images/level{level}_data"):
        pickle_in = open(f"../images/level{level}_data", 'rb')
        world_data = pickle.load(pickle_in)
    world = World(world_data)

    # Создание фиктивной монеты для отображения результатов
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world


class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False

        # Получаем положение мыши
        pos = pygame.mouse.get_pos()

        # Проверяем правильность наведения курсора мыши и щелкаем
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True

        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False

        # рисуем кнопку
        screen.blit(self.image, self.rect)

        return action


class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def handle_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.locals.K_SPACE] and not self.jumped and not self.in_air:
            jump_fx.play()
            self.vel_y = -15
            self.jumped = True
        if not keys[pygame.locals.K_SPACE]:
            self.jumped = False
        if keys[pygame.locals.K_LEFT]:
            self.dx -= 5
            self.counter += 1
            self.direction = -1
        if keys[pygame.locals.K_RIGHT]:
            self.dx += 5
            self.counter += 1
            self.direction = 1
        if not keys[pygame.locals.K_LEFT] and not keys[pygame.locals.K_RIGHT]:
            self.counter = 0
            self.index = 0
            self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]

    def handle_animation(self):
        walk_cooldown = 5
        if self.counter > walk_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images_right):
                self.index = 0
            self.image = self.images_right[self.index] if self.direction == 1 else self.images_left[self.index]

    def handle_collisions_with_tiles(self):
        for tile in world.tile_list:
            if tile[1].colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
            if tile[1].colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                if self.vel_y < 0:
                    self.dy = tile[1].bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = tile[1].top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False

    def handle_collisions_with_platforms(self):
        for platform in platform_group:
            if platform.rect.colliderect(self.rect.x + self.dx, self.rect.y, self.width, self.height):
                self.dx = 0
            if platform.rect.colliderect(self.rect.x, self.rect.y + self.dy, self.width, self.height):
                if self.vel_y < 0:
                    self.dy = platform.rect.bottom - self.rect.top
                    self.vel_y = 0
                elif self.vel_y >= 0:
                    self.dy = platform.rect.top - self.rect.bottom
                    self.vel_y = 0
                    self.in_air = False
                    self.rect.x += platform.move_direction * platform.move_x
                    self.rect.y += platform.move_direction * platform.move_y

    def handle_vertical_movement(self):
        self.vel_y += 1
        if self.vel_y > 10:
            self.vel_y = 10
        self.dy += self.vel_y
        self.in_air = True

    def handle_movement(self):
        self.handle_vertical_movement()
        self.handle_collisions_with_tiles()
        self.handle_collisions_with_platforms()

    def update(self, game_over):
        if game_over == 0:
            self.dx, self.dy = 0, 0
            self.handle_input()
            self.handle_animation()
            self.handle_movement()

            self.rect.x += self.dx
            self.rect.y += self.dy

            # Проверка столкновения с противниками
            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1  # Игрок умер

            # Проверка столкновения с лавой
            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1  # Игрок умер

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, blue, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)

        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 4):
            img_right = pygame.image.load(f"../images/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load("../images/ghost.png")
        self.image = self.images_right[self.index]
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.vel_y = 0
        self.jumped = False
        self.direction = 0
        self.in_air = True


class World():
    def __init__(self, data):
        self.tile_list = []
        self.load_tiles(data)

    def load_tiles(self, data):
        # Load images
        dirt_img = pygame.image.load("../images/dirt.png")
        grass_img = pygame.image.load("../images/grass.png")

        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    self.add_tile(dirt_img, col_count, row_count)
                elif tile == 2:
                    self.add_tile(grass_img, col_count, row_count)
                elif tile == 3:
                    self.add_enemy(col_count, row_count)
                elif tile == 4:
                    self.add_platform(col_count, row_count, 1, 0)
                elif tile == 5:
                    self.add_platform(col_count, row_count, 0, 1)
                elif tile == 6:
                    self.add_lava(col_count, row_count)
                elif tile == 7:
                    self.add_coin(col_count, row_count)
                elif tile == 8:
                    self.add_exit(col_count, row_count)
                col_count += 1
            row_count += 1

    def add_tile(self, image, col, row):
        img = pygame.transform.scale(image, (tile_size, tile_size))
        img_rect = img.get_rect()
        img_rect.x = col * tile_size
        img_rect.y = row * tile_size
        self.tile_list.append((img, img_rect))

    def add_enemy(self, col, row):
        blob = Enemy(col * tile_size, row * tile_size + 15)
        blob_group.add(blob)

    def add_platform(self, col, row, move_x, move_y):
        platform = Platform(col * tile_size, row * tile_size, move_x, move_y)
        platform_group.add(platform)

    def add_lava(self, col, row):
        lava = Lava(col * tile_size, row * tile_size + (tile_size // 2))
        lava_group.add(lava)

    def add_coin(self, col, row):
        coin = Coin(col * tile_size + (tile_size // 2), row * tile_size + (tile_size // 2))
        coin_group.add(coin)

    def add_exit(self, col, row):
        exit_sprite = Exit(col * tile_size, row * tile_size - (tile_size // 2))
        exit_group.add(exit_sprite)

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])


class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("../images/blob.png")
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_direction = 1
        self.move_counter = 0

    def update(self):
        self.rect.x += self.move_direction
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("../images/platform.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.move_counter = 0
        self.move_direction = 1
        self.move_x = move_x
        self.move_y = move_y

    def update(self):
        self.rect.x += self.move_direction * self.move_x
        self.rect.y += self.move_direction * self.move_y
        self.move_counter += 1
        if abs(self.move_counter) > 50:
            self.move_direction *= -1
            self.move_counter *= -1


class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("../images/lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("../images/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)


class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("../images/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


player = Player(100, screen_height - 130)

blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()

# Создание фиктивной монетки для отображения счета
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

# Загрузка данных уровня и создание мира
if path.exists(f"../images/level{level}_data"):
    pickle_in = open(f"../images/level{level}_data", 'rb')
    world_data = pickle.load(pickle_in)
world = World(world_data)


# Создание кнопок
restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)


run = True
while run:

    clock.tick(fps)

    screen.blit(bg_img, (0, 0))
    screen.blit(sun_img, (100, 100))

    if main_menu:
        if exit_button.draw():
            run = False
        if start_button.draw():
            main_menu = False
    else:
        world.draw()

        if game_over == 0:
            blob_group.update()
            platform_group.update()
            # Обновление счета
            # Проверка, собрана ли монетка
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text('X ' + str(score), font_score, white, tile_size - 10, 10)

        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        # Если игрок умер
        if game_over == -1:
            if restart_button.draw():
                world_data = []
                world = reset_level(level)
                game_over = 0
                score = 0

        # Если игрок приближается к порталу
        if pygame.sprite.spritecollide(player, exit_group, False):
            # Переход на следующий уровень
            game_over = 1

        # Если игрок завершил уровень
        if game_over == 1:
            # Сброс игры и переход на следующий уровень
            level += 1
            if level <= max_levels:
                # Сброс уровня
                world_data = []
                world = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, blue, (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    # Сброс уровня
                    world_data = []
                    world = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()