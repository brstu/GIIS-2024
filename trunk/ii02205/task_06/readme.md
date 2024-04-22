# Лабораторная работа № 6

## Создание анимации

## Цель работы 
Изучить Создание анимации.

## Ход работы
В ходе работы над лабораторной работой была реализована анимация.

## Код программы
[main.py](./src/main.py) (отвечает за запуск приложения приложения)
```python
from animation import App


def main():
    app = App()
    app.work()


if __name__ == "__main__":
    main()
```
[animation.py](./src/animation.py)
```python
import pygame
import sys
import numpy as np
from math import pi, cos, sin, sqrt, atan2
import random
import scipy


def bezier(points: np.array) -> tuple:
    pass
    return x, y


radius = 150


def get_round_coords(n: int) -> np.array:
    pass
    return result


class App:

    def __init__(self):
        pass

    def set_new_points(self) -> None:

        pass

    def get_current_points(self) -> np.array:
        pass
        return res

    def work(self) -> None:
        pass

    def blur_surface(self) -> pygame.Surface:
        pass
        return new_surface
```


## Результаты работы
Референс

![](./images/reference.gif)

Результат

![](./images/animation.gif)
