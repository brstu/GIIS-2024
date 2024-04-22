import pygame
import sys
import numpy as np
from math import pi, cos, sin, sqrt, atan2
import random
import scipy
import secrets

def bezier(points: np.array) -> tuple:
    first_x = points[0, 0]
    second_x = points[1, 0]
    third_x = points[2, 0]

    first_y = points[0, 1]
    second_y = points[1, 1]
    third_y = points[2, 1]
    t = np.linspace(0, 1)

    x = first_x * (t ** 2) + 2 * t * (1 - t) * second_x + (1 - t) ** 2 * third_x
    y = first_y * (t ** 2) + 2 * t * (1 - t) * second_y + (1 - t) ** 2 * third_y

    return x, y

bits = 20
radius = 150


def get_round_coords(n: int) -> np.array:
    result = np.zeros((n, 2))
    for i in range(n):
        angle = 2 * pi / n * i
        result[i, 0] = radius * cos(angle)
        result[i, 1] = radius * sin(angle)
    return result


class App:

    def __init__(self):
        pygame.init()
        self.screen_width = 500
        self.screen_height = 500
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.surface = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
        pygame.display.set_caption("Animation")
        self.counter = -1
        self.fps = 100
        self.clock = pygame.time.Clock()
        self.rng = np.random.default_rng(seed=42)
        self.n = 10

        self.points_prev = get_round_coords(self.n)
        self.points_new = get_round_coords(self.n)
        self.t_prev = self.rng.random((self.n, 1))
        self.t_new = np.copy(self.t_prev)

        self.delta = np.zeros_like(self.points_prev)
        self.delta_t = np.zeros_like(self.t_prev)

    def set_new_points(self) -> None:

        self.points_prev = np.copy(self.points_new)
        self.t_prev = np.copy(self.t_new)

        threshold = 0.3
        self.t_new = self.rng.random((self.n, 1)) * (1 - 2 * threshold) + threshold

        self.delta = np.zeros_like(self.points_prev)
        self.delta_t = self.t_new - self.t_prev
        common_angle = 5 / 360 * 2 * pi  # * random.random()

        for i in range(self.n):
            x = self.points_prev[i, 0]
            y = self.points_prev[i, 1]
            r = sqrt(x ** 2 + y ** 2)
            angle = atan2(y, x)

            new_angle = angle + common_angle
            delta_r = 40 * ((secrets.randbits(bits) / (2 ** bits)) * 2 - 1) * 40

            if r + delta_r > radius * 1.5 or r + delta_r < radius * 0.55:
                r -= 0.05 * delta_r * 0
            else:
                r += delta_r

            self.delta[i, 0] = r * cos(new_angle) - x
            self.delta[i, 1] = r * sin(new_angle) - y
        self.points_new = np.copy(self.points_prev) + self.delta

    def get_current_points(self) -> np.array:

        percent = self.counter / (1 * self.fps - 1)

        current_points = self.points_prev + percent * self.delta
        current_t = self.t_prev + percent * self.delta_t

        median_points = current_points * current_t + (1 - current_t) * np.roll(current_points, -1, axis=0)

        res = np.zeros((2 * self.n, 2))

        for i in range(self.n):
            res[i * 2] = current_points[i]
            res[i * 2 + 1] = median_points[i]

        res = np.roll(res, -1, axis=0)
        res = np.concatenate((res, res[0:1]), axis=0)
        res += np.array([[self.screen_width / 2, self.screen_height / 2]])
        return res

    def work(self) -> None:

        running = True
        while running:
            self.counter = (self.counter + 1) % (1 * self.fps)

            if self.counter == 0:
                self.set_new_points()
            self.surface.fill((25, 25, 25, 255))
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            curr_points = self.get_current_points()

            points = []
            color = (77, 238, 234, 255)
            for k in range(self.n):
                x, y = bezier(curr_points[0 + 2 * k: 3 + 2 * k, :])
                temp_points = []
                for i in range(len(x) - 1):
                    pygame.draw.line(self.surface, color, (x[i], y[i]), (x[i + 1], y[i + 1]), 2)
                    temp_points.append((x[i], y[i]))
                points.extend(temp_points[::-1])
            pygame.draw.polygon(self.surface, color, points)

            self.screen.blit(self.blur_surface(), (0, 0))
            pygame.display.flip()
            pygame.display.set_caption(f"FPS: {int(self.clock.get_fps())}")
            self.clock.tick(1 * self.fps)

        pygame.quit()
        sys.exit()

    def blur_surface(self) -> pygame.Surface:
        array = pygame.surfarray.pixels3d(self.surface).copy()
        blurred_array = np.zeros_like(array)
        radius_gaus = 15
        blurred_array[:, :, 0] = scipy.ndimage.gaussian_filter(array[:, :, 0], sigma=radius_gaus)
        blurred_array[:, :, 1] = scipy.ndimage.gaussian_filter(array[:, :, 1], sigma=radius_gaus)
        blurred_array[:, :, 2] = scipy.ndimage.gaussian_filter(array[:, :, 2], sigma=radius_gaus)
        new_surface = pygame.surfarray.make_surface(blurred_array)
        return new_surface
