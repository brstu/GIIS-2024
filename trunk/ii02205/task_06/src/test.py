import pygame
import sys
import numpy as np
from math import pi, cos, sin

def bezier(points: np.array):
    first_x = points[0, 0]
    second_x = points[0, 1]
    third_x = points[0, 2]

    first_y = points[1, 0]
    second_y = points[1, 1]
    third_y = points[1, 2]
    t = np.linspace(0, 1)

    x = first_x * (t ** 2) + 2 * t * (1 - t) * second_x + (1 - t) ** 2 * third_x
    y = first_y * (t ** 2) + 2 * t * (1 - t) * second_y + (1 - t) ** 2 * third_y

    return x, y


radius = 200

def get_round_coords(n: int) -> np.array:
    result = np.zeros((2, n))
    for i in range(n):
        angle = 2 * pi / n * i
        result[0, i] = radius * cos(angle)
        result[1, i] = radius * sin(angle)
    return result
class App:



    def __init__(self):
        pygame.init()
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Animation")
        self.counter = 0
        self.fps = 100
        self.clock = pygame.time.Clock()

        self.n = 10
        self.points_prev = get_round_coords(self.n) + np.array([[self.screen_width / 2], [self.screen_height / 2]])
        self.t_prev = np.random.rand(1, self.n)

        self.points_new = self.points_prev + (np.random.rand(2, self.n) * 2 - 1) * 100
        self.t_new = np.random.rand(1, self.n)

        self.delta_points = (self.points_new - self.points_prev) / (2 * self.fps)
        self.delta_t = (self.t_new - self.t_prev) / (2 * self.fps)



    def set_new_points(self):


        self.points_prev = np.copy(self.points_new)
        self.t_prev = np.copy(self.t_new)

        self.points_new = self.points_prev + (np.random.rand(2, self.n) * 2 - 1) * 100
        self.t_new = np.random.rand(1, self.n)

        self.delta_points = (self.points_new - self.points_prev) / (2 * self.fps)
        self.delta_t = (self.t_new - self.t_prev) / (2 * self.fps)

    def get_current_points(self):

        percent = (self.counter + 1)

        self.current_points = self.points_prev + percent * self.delta_points
        self.current_t = self.t_prev + percent * self.delta_t

        median_points = self.current_points * self.current_t + (1 - self.current_t) * np.roll(self.current_points, -1, axis=1)

        res = np.concatenate((np.reshape(self.current_points, (2 * self.n, 1)), np.reshape(median_points, (2 * self.n, 1))), axis=1)
        res = np.reshape(res, (2, 2 * self.n))
        res = np.roll(res, -1, axis=1)
        res = np.concatenate((res, res[:, 0:1]), axis=1)
        return res


    def work(self):

        running = True
        while running:
            self.counter = (self.counter + 1) % (2 * self.fps)
            if self.counter == 0:
                self.set_new_points()
                pass
            self.screen.fill((0,0,0))
            # Обработка событий
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            curr_points = self.get_current_points()
            print(self.counter, curr_points[0][0])

            # for i in range(2 * self.n):
            #     pygame.draw.line(self.screen, (120, 255 / (2 * self.n) * i, 0), (curr_points[0, i], curr_points[1, i]),
            #                      (curr_points[0, i + 1], curr_points[1, i + 1]), 10)

            for k in range(self.n):
                x, y = bezier(curr_points[:, 0 + 2 * k: 3 + 2 * k])
                for i in range(len(x) - 1):
                    pygame.draw.line(self.screen, (0, 0, 255), (x[i], y[i]), (x[i + 1], y[i + 1]), 2)


            # Обновление экрана
            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")

            # Ограничение кадров в секунду
            self.clock.tick(self.fps)

        # Завершение работы Pygame
        pygame.quit()
        sys.exit()
