import sys
import cv2
import numpy as np
from math import floor


def median_filter(params: tuple) -> None:
    image: np.ndarray = params[0]
    size: int = params[1]
    horizontal: bool = params[2]
    vertical: bool = params[3]
    height, width = image.shape
    cv2.imshow('before', image)
    if size % 2 == 0:
        size += 1
    half_size = floor(size / 2)

    half_size_x = half_size
    half_size_y = half_size

    if not horizontal:
        half_size_x = 0
    if not vertical:
        half_size_y = 0
    for x in range(half_size_x, width - half_size_x):
        for y in range(half_size_y, height - half_size_y):
            subimage = image[y - half_size_y: y + half_size_y + 1, x - half_size_x: x + half_size_x + 1]
            count = subimage.shape[0] * subimage.shape[1]
            values = np.resize(subimage, (1, count))
            sorted_values = np.sort(values)
            median_value = sorted_values[0][floor(count / 2)]
            image[y, x] = median_value
    cv2.imshow('after', image)
    cv2.imwrite('result.jpg', image)
    cv2.waitKey(0)


def check_input_params():
    if len(sys.argv) >= 5:
        file_path = sys.argv[1]
        flag1 = sys.argv[2]
        flag2 = sys.argv[3]
        size = sys.argv[4]
        if flag1.lower() == "false":
            flag1 = False
        elif flag1.lower() == "true":
            flag1 = True
        else:
            return None

        if flag2.lower() == "false":
            flag2 = False
        elif flag2.lower() == "true":
            flag2 = True
        else:
            return None

        if not size.isnumeric():
            return None
        size = int(size)

        try:
            with open(file_path, 'r') as _:
                print("Все ок сейчас все пофильтрую")
        except FileNotFoundError:
            return None
        image = cv2.imread(file_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return image, size, flag1, flag2


def main():
    params = check_input_params()
    if params is not None:
        median_filter(params)
    else:
        print("Параметры не те или файл не найден \nПример запуска скрипта - 'python main.py [имя файла] [фильтрация по горизонтали(true/false)]"
              " [фильтрация по вертикали(true/false)] [размер для фильтра]'")


if __name__ == "__main__":
    main()
