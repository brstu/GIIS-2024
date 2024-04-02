import random
import pygame
import numpy as np
from math import ceil
from moving import moving_pattern

fps = 60
window_size = (1000, 1000)
player = pygame.image.load("../images/player1.png")
invader_1 = pygame.image.load("../images/invador_4.png")
invader_2 = pygame.image.load("../images/invador_5.png")
invader_3 = pygame.image.load("../images/invador_6.png")


class Shoot:
    is_correct: bool = True
    is_player_shoot: bool
    direction: np.array
    position: np.array

    def __init__(self, position: np.array, is_players_shoot: bool):
        self.position = np.array(position)
        self.direction = np.array([0, -5])
        self.direction[1] = -5 * (1 if is_players_shoot else -1)
        self.is_player_shoot = is_players_shoot

    def move(self):
        self.position += self.direction
        if self.position[1] < 0 or self.position[1] > window_size[1]:
            self.is_correct = False


class Player:
    size: np.array = np.array([25, 25])
    lives: int = 3
    position: np.array = np.array([window_size[0] / 2, window_size[1] - 100])
    score: int = 0

    def __init__(self):
        self.speed: int = 5
        self.cooldown_tick: int = 0

    def update_position(self, direction: bool):
        if not direction and (self.position[0] - self.size[0]) > self.speed:
            self.position[0] -= self.speed
        if direction and (self.position[0] + self.size[0]) < window_size[0] - self.speed:
            self.position[0] += self.speed

    def decrement_cooldown(self):
        if self.cooldown_tick != 0:
            self.cooldown_tick -= 1


class Invador:
    position: np.array
    type_of_person: int
    size: int = 20
    is_destroyed: bool = False

    def __init__(self, row_index: int, column_index: int):
        match row_index:
            case 0:
                self.type_of_person = 2
            case 1:
                self.type_of_person = 1
            case 2:
                self.type_of_person = 1
            case 3:
                self.type_of_person = 0
            case 4:
                self.type_of_person = 0

        step = window_size[0] / (11 + 8)
        self.position = np.array([step * (column_index + 4), row_index * 50 + 2 * step + self.size])


class Block:
    size: tuple = (51, 51)

    matrix_of_block: np.array
    center: np.array

    def __init__(self, column_index: int):

        step = (window_size[0] - 200) / 5

        self.center = [100 + column_index * step, window_size[1] - 200]
        self.matrix_of_block = np.ones((self.size[1], self.size[0]))

    def collision_detection(self, shoot: Shoot) -> bool:
        first_pos = shoot.position
        second_pos = shoot.position + shoot.direction
        x = int(first_pos[0] - self.center[0] + self.size[0] // 2)
        first_y = min(first_pos[1] - self.center[1] + self.size[1] // 2,
                      second_pos[1] - self.center[1] + self.size[1] // 2)
        second_y = max(first_pos[1] - self.center[1] + self.size[1] // 2,
                       second_pos[1] - self.center[1] + self.size[1] // 2)
        for y in range(int(first_y), int(second_y + 1)):
            if 0 <= y < self.size[1]:
                if np.sum(self.matrix_of_block[x - 2: x + 2, y]) >= 1:
                    x_indices, y_indices = np.indices(self.matrix_of_block.shape)
                    circle_mask = (x_indices - x) ** 2 + (y_indices - y) ** 2 <= 7 ** 2
                    self.matrix_of_block[circle_mask] = 0
                    return True
        return False


class Game:
    is_begining: bool = False
    is_running: bool = False
    is_gameover: bool = False
    is_gamewin: bool = False
    is_paused: bool = False

    player: Player = Player()
    blocks: list[Block]
    invadors: list[Invador]
    shoots: list[Shoot]
    ticks_for_move: list

    def __init__(self):
        self.start_game()

    def start_game(self):
        self.is_begining = True
        self.is_running = True
        self.blocks = []
        self.shoots = []
        self.invadors = []
        self.ticks_for_move = [30, 0]
        self.player = Player()

        for i in range(11):
            for j in range(5):
                self.invadors.append(Invador(j, i))
        for i in range(6):
            self.blocks.append(Block(i))

    def game_tick(self):
        if not self.is_begining or not self.is_running:
            return None
        self.player.decrement_cooldown()
        self.shoot_collision()
        if self.ticks_for_move[0] > 0:
            self.ticks_for_move[0] -= 1

        if self.ticks_for_move[0] == 0:
            moving = moving_pattern[self.ticks_for_move[1]]
            self.invadors_move(moving)
            self.ticks_for_move = [int(30 - (27 * (55 - len(self.invadors)) / 55)),
                                   (self.ticks_for_move[1] + 1) % len(moving_pattern)].copy()

    def add_player_shot(self):
        if self.player.cooldown_tick == 0:
            self.player.cooldown_tick = 30
            self.shoots.append(Shoot(self.player.position, True))

    def add_invadors_shoots(self):
        for invador in self.invadors:
            if abs(invador.position[0] - self.player.position[0]) < self.player.size[0] and random.random() < 0.125:
                self.shoots.append(Shoot(invador.position, False))

    def player_minus_live(self):
        if self.player.lives > 0:
            self.player.lives -= 1
        if self.player.lives == 0:
            self.game_over()

    def shot_collision_with_blocks(self, shoot: Shoot):
        for block in self.blocks:
            if (block.center[0] - block.size[0] // 2 - 3 <= shoot.position[0] <
                    block.center[0] + block.size[0] // 2 + 3):
                if block.collision_detection(shoot):
                    shoot.is_correct = False
                    break

    def shoot_collision_with_invadors(self, shoot: Shoot, first_pos: np.array, second_pos: np.array):
        for invador in self.invadors:
            if (min(int(first_pos[1]), int(second_pos[1])) <= invador.position[1]
                    <= max(int(first_pos[1]), int(second_pos[1]))
                    and abs(first_pos[0] - invador.position[0]) < invador.size):
                invador.is_destroyed = True
                shoot.is_correct = False
                self.player.score += (invador.type_of_person + 1) * 10

    def shoot_collision_with_player(self, shoot: Shoot, first_pos: np.array, second_pos: np.array):
        if (min(int(first_pos[1]), int(second_pos[1])) <= self.player.position[1]
                <= max(int(first_pos[1]), int(second_pos[1]))
                and abs(first_pos[0] - self.player.position[0]) < self.player.size[0]):
            self.player_minus_live()
            shoot.is_correct = False

    def shoot_collision(self):
        for shoot in self.shoots:
            self.shot_collision_with_blocks(shoot)
            if shoot.is_correct:
                first_pos = shoot.position.copy()
                second_pos = [shoot.position[0] + shoot.direction[0], shoot.position[1] + shoot.direction[1]].copy()
                if shoot.is_player_shoot:
                    self.shoot_collision_with_invadors(shoot, first_pos, second_pos)
                else:
                    self.shoot_collision_with_player(shoot, first_pos, second_pos)

        if len(self.invadors) == 0:
            self.game_win()

    def game_win(self):
        self.is_gamewin = True

    def game_over(self):
        self.is_gameover = True

    def invadors_move(self, direction: np.array):
        for invador in self.invadors:
            if invador.type_of_person in [0, 1, 2]:
                invador.position += direction
                if invador.position[1] > window_size[1] - 200:
                    self.game_over()


class App:
    is_running: bool = True
    clock: pygame.time.Clock = pygame.time.Clock()
    game: Game = Game()
    ticks: int = 0
    font: pygame.font.Font

    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(window_size)
        self.screen.fill((255, 0, 0))
        pygame.display.flip()
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.game.start_game()

    def quit(self):
        self.is_running = False

    def process_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                self.game.is_paused = not self.game.is_paused
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.game.player.update_position(False)
        if keys[pygame.K_RIGHT]:
            self.game.player.update_position(True)
        if keys[pygame.K_UP]:
            self.game.add_player_shot()

    def draw_shoots(self):
        for shoot in self.game.shoots:
            shoot.move()
            if shoot.is_correct:
                if shoot.is_player_shoot:
                    pygame.draw.circle(self.screen, (0, 255, 0), shoot.position, 5)
                else:
                    pygame.draw.circle(self.screen, (255, 255, 255), shoot.position, 5)

    def draw_invadors(self):
        for invador in self.game.invadors:
            if not invador.is_destroyed:
                pos = invador.position - [invador.size, invador.size]
                if invador.type_of_person == 0:
                    self.screen.blit(invader_1, (pos[0], pos[1]))
                elif invador.type_of_person == 1:
                    self.screen.blit(invader_2, (pos[0], pos[1]))
                elif invador.type_of_person == 2:
                    self.screen.blit(invader_3, (pos[0], pos[1]))

    def work(self):
        while self.is_running:
            self.process_keys()
            self.screen.fill((0, 0, 0))
            if self.game.is_gameover:
                text = self.font.render('Game Over', True, (255, 255, 255), (0, 0, 0))
                text_rect = text.get_rect()
                text_rect.center = (window_size[0] / 2, window_size[1] / 2)
                self.screen.blit(text, text_rect)
            elif self.game.is_gamewin:
                win_text = self.font.render('Game Win!!!', True, (125, 255, 125), (0, 0, 0))
                score_text = self.font.render(f'Score: {self.game.player.score}', True, (125, 255, 125), (0, 0, 0))
                win_text_rect = win_text.get_rect()
                score_text_rect = score_text.get_rect()
                win_text_rect.center = (window_size[0] / 2, window_size[1] / 2)
                score_text_rect.center = (window_size[0] / 2,
                                          (window_size[1] + score_text_rect.height + win_text_rect.height) / 2)
                self.screen.blit(win_text, win_text_rect)
                self.screen.blit(score_text, score_text_rect)
            elif self.game.is_paused:
                win_text = self.font.render('Paused', True, (255, 255, 255), (0, 0, 0))
                win_text_rect = win_text.get_rect()
                win_text_rect.center = (window_size[0] / 2, window_size[1] / 2)
                self.screen.blit(win_text, win_text_rect)
            else:

                self.game.game_tick()

                for block in self.game.blocks:
                    a = pygame.surfarray.make_surface(block.matrix_of_block)
                    pos = block.center.copy()
                    pos[0] -= ceil(block.size[0] / 2)
                    pos[1] -= ceil(block.size[1] / 2)
                    self.screen.blit(a, pos)

                pos = self.game.player.position - self.game.player.size

                self.screen.blit(player, (pos[0], pos[1]))

                self.draw_shoots()

                self.game.shoots = [shoot for shoot in self.game.shoots if shoot.is_correct]

                if self.ticks in [0, 30]:
                    self.game.add_invadors_shoots()

                self.draw_invadors()

                self.game.invadors = [invador for invador in self.game.invadors if not invador.is_destroyed]

                lives = self.font.render(f'{self.game.player.lives}', True, (255, 255, 255), (0, 0, 0))
                lives_rect = lives.get_rect()
                lives_rect.center = (lives_rect.width // 2, window_size[1] - lives_rect.height // 2)
                self.screen.blit(lives, lives_rect)

                score = self.font.render(f'{self.game.player.score}', True, (255, 255, 255), (0, 0, 0))
                score_rect = score.get_rect()
                score_rect.center = (window_size[0] - score_rect.width // 2, window_size[1] - score_rect.height // 2)
                self.screen.blit(score, score_rect)
            pygame.display.flip()
            self.clock.tick(fps)
            self.ticks = (self.ticks + 1) % fps
