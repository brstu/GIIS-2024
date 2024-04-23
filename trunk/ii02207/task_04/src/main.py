import pygame
from pygame.locals import KEYDOWN, K_SPACE, K_LEFT, K_RIGHT
from pygame import mixer
import pickle
from os import path

# Инициализация Pygame
pygame.mixer.pre_init(44100, -16, 2, 512)
mixer.init()
pygame.init()

# Определение экрана
screen_width = 1000
screen_height = 1000
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Platformer')

# Определение констант
FPS = 60
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
MAX_LEVELS = 7

# Загрузка изображений
sun_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/sun.png")
bg_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/sky.png")
restart_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/restart_btn.png")
start_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/start_btn.png")
exit_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/exit_btn.png")

# Загрузка звуков
pygame.mixer.music.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/music.wav")
pygame.mixer.music.play(-1, 0.0, 5000)
coin_fx = pygame.mixer.Sound("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/coin.wav")
coin_fx.set_volume(0.5)
jump_fx = pygame.mixer.Sound("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/jump.wav")
jump_fx.set_volume(0.5)
game_over_fx = pygame.mixer.Sound("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/game_over.wav")
game_over_fx.set_volume(0.5)

# Определение шрифтов
font = pygame.font.SysFont('Bauhaus 93', 70)
font_score = pygame.font.SysFont('Bauhaus 93', 30)

# Определение игровых переменных
tile_size = 50
game_over = 0
main_menu = True
level = 3
score = 0

# Класс кнопки
class Button():
    def __init__(self, x, y, image):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.clicked = False

    def draw(self):
        action = False
        pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(pos):
            if pygame.mouse.get_pressed()[0] == 1 and not self.clicked:
                action = True
                self.clicked = True
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        screen.blit(self.image, self.rect)
        return action

# Класс игрока
class Player():
    def __init__(self, x, y):
        self.reset(x, y)

    def update(self, game_over):
        dx = 0
        dy = 0
        walk_cooldown = 5
        col_thresh = 20

        if game_over == 0:
            keys = pygame.key.get_pressed()
            if keys[K_SPACE] and not self.jumped and not self.in_air:
                jump_fx.play()
                self.vel_y = -15
                self.jumped = True
            if not keys[K_SPACE]:
                self.jumped = False
            if keys[K_LEFT]:
                dx -= 5
                self.counter += 1
                self.direction = -1
            if keys[K_RIGHT]:
                dx += 5
                self.counter += 1
                self.direction = 1
            if not keys[K_LEFT] and not keys[K_RIGHT]:
                self.counter = 0
                self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]
            if self.counter > walk_cooldown:
                self.counter = 0    
                self.index += 1
                if self.index >= len(self.images_right):
                    self.index = 0
                if self.direction == 1:
                    self.image = self.images_right[self.index]
                if self.direction == -1:
                    self.image = self.images_left[self.index]

            self.vel_y += 1
            if self.vel_y > 10:
                self.vel_y = 10
            dy += self.vel_y

            self.in_air = True
            for tile in world.tile_list:
                if tile[1].colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if tile[1].colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if self.vel_y < 0:
                        dy = tile[1].bottom - self.rect.top
                        self.vel_y = 0
                    elif self.vel_y >= 0:
                        dy = tile[1].top - self.rect.bottom
                        self.vel_y = 0
                        self.in_air = False

            if pygame.sprite.spritecollide(self, blob_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, lava_group, False):
                game_over = -1
                game_over_fx.play()

            if pygame.sprite.spritecollide(self, exit_group, False):
                game_over = 1

            for platform in platform_group:
                if platform.rect.colliderect(self.rect.x + dx, self.rect.y, self.width, self.height):
                    dx = 0
                if platform.rect.colliderect(self.rect.x, self.rect.y + dy, self.width, self.height):
                    if abs((self.rect.top + dy) - platform.rect.bottom) < col_thresh:
                        self.vel_y = 0
                        dy = platform.rect.bottom - self.rect.top
                    elif abs((self.rect.bottom + dy) - platform.rect.top) < col_thresh:
                        self.rect.bottom = platform.rect.top - 1
                        self.in_air = False
                        dy = 0
                    if platform.move_x != 0:
                        self.rect.x += platform.move_direction

            self.rect.x += dx
            self.rect.y += dy

        elif game_over == -1:
            self.image = self.dead_image
            draw_text('GAME OVER!', font, BLUE, (screen_width // 2) - 200, screen_height // 2)
            if self.rect.y > 200:
                self.rect.y -= 5

        screen.blit(self.image, self.rect)
        return game_over

    def reset(self, x, y):
        self.images_right = []
        self.images_left = []
        self.index = 0
        self.counter = 0
        for num in range(1, 5):
            img_right = pygame.image.load(f"D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/guy{num}.png")
            img_right = pygame.transform.scale(img_right, (40, 80))
            img_left = pygame.transform.flip(img_right, True, False)
            self.images_right.append(img_right)
            self.images_left.append(img_left)
        self.dead_image = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/ghost.png")
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

# Класс мира
class World():
    def __init__(self, data):
        self.tile_list = []
        dirt_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/dirt.png")
        grass_img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/grass.png")
        row_count = 0
        for row in data:
            col_count = 0
            for tile in row:
                if tile == 1:
                    img = pygame.transform.scale(dirt_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 2:
                    img = pygame.transform.scale(grass_img, (tile_size, tile_size))
                    img_rect = img.get_rect()
                    img_rect.x = col_count * tile_size
                    img_rect.y = row_count * tile_size
                    tile = (img, img_rect)
                    self.tile_list.append(tile)
                if tile == 3:
                    blob = Enemy(col_count * tile_size, row_count * tile_size + 15)
                    blob_group.add(blob)
                if tile == 4:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 1, 0)
                    platform_group.add(platform)
                if tile == 5:
                    platform = Platform(col_count * tile_size, row_count * tile_size, 0, 1)
                    platform_group.add(platform)
                if tile == 6:
                    lava = Lava(col_count * tile_size, row_count * tile_size + (tile_size // 2))
                    lava_group.add(lava)
                if tile == 7:
                    coin = Coin(col_count * tile_size + (tile_size // 2), row_count * tile_size + (tile_size // 2))
                    coin_group.add(coin)
                if tile == 8:
                    exit_sprite = Exit(col_count * tile_size, row_count * tile_size - (tile_size // 2))
                    exit_group.add(exit_sprite)
                col_count += 1
            row_count += 1

    def draw(self):
        for tile in self.tile_list:
            screen.blit(tile[0], tile[1])

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/blob.png")
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

# Класс платформы
class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, move_x, move_y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/platform.png")
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

# Класс лавы
class Lava(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/lava.png")
        self.image = pygame.transform.scale(img, (tile_size, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Класс монеты
class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/coin.png")
        self.image = pygame.transform.scale(img, (tile_size // 2, tile_size // 2))
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

# Класс выхода
class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        img = pygame.image.load("D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/images/exit.png")
        self.image = pygame.transform.scale(img, (tile_size, int(tile_size * 1.5)))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

# Функция сброса уровня
def reset_level(level):
    player.reset(100, screen_height - 130)
    blob_group.empty()
    platform_group.empty()
    coin_group.empty()
    lava_group.empty()
    exit_group.empty()

    if path.exists(f"D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/level{level}_data"):
        with open(f"D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/level{level}_data", 'rb') as pickle_in:
            world_data = pickle.load(pickle_in)
    world = World(world_data)
    score_coin = Coin(tile_size // 2, tile_size // 2)
    coin_group.add(score_coin)
    return world, world_data

# Добавление импорта для clock
clock = pygame.time.Clock()

# Определение функции draw_text
def draw_text(text, font, color, x, y):
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, (x, y))

player = Player(100, screen_height - 130)
blob_group = pygame.sprite.Group()
platform_group = pygame.sprite.Group()
lava_group = pygame.sprite.Group()
coin_group = pygame.sprite.Group()
exit_group = pygame.sprite.Group()
score_coin = Coin(tile_size // 2, tile_size // 2)
coin_group.add(score_coin)

if path.exists(f"D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/level{level}_data"):
    with open(f"D:/6 семестр/ГИИС лабы/GIIS-2024/trunk/ii02207/task_04/level{level}_data", 'rb') as pickle_in:
        world_data = pickle.load(pickle_in)
world = World(world_data)

restart_button = Button(screen_width // 2 - 50, screen_height // 2 + 100, restart_img)
start_button = Button(screen_width // 2 - 350, screen_height // 2, start_img)
exit_button = Button(screen_width // 2 + 150, screen_height // 2, exit_img)

run = True
while run:
    clock.tick(FPS)
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
            if pygame.sprite.spritecollide(player, coin_group, True):
                score += 1
                coin_fx.play()
            draw_text('X ' + str(score), font_score, WHITE, tile_size - 10, 10)
        
        blob_group.draw(screen)
        platform_group.draw(screen)
        lava_group.draw(screen)
        coin_group.draw(screen)
        exit_group.draw(screen)

        game_over = player.update(game_over)

        if game_over == -1:
            if restart_button.draw():
                world, world_data = reset_level(level)
                game_over = 0
                score = 0

        if game_over == 1:
            level += 1
            if level <= MAX_LEVELS:
                world, world_data = reset_level(level)
                game_over = 0
            else:
                draw_text('YOU WIN!', font, BLUE, (screen_width // 2) - 140, screen_height // 2)
                if restart_button.draw():
                    level = 1
                    world, world_data = reset_level(level)
                    game_over = 0
                    score = 0

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()

pygame.quit()