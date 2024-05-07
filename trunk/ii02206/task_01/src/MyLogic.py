from PIL import Image, ImageDraw
import numpy as np
import os
import tkinter


def create_noise(image_path, factor):
    """
    Создает шум на изображении и сохраняет его.
    """
    image = Image.open(image_path)
    draw = ImageDraw.Draw(image)
    width, height = image.size
    pixels = image.load()

    for i in range(width):
        for j in range(height):
            rand = np.random.randint(-factor, factor)
            a = pixels[i, j][0] + rand
            b = pixels[i, j][1] + rand
            c = pixels[i, j][2] + rand
            a = 0 if a < 0 else 255 if a > 255 else a
            b = 0 if b < 0 else 255 if b > 255 else b
            c = 0 if c < 0 else 255 if c > 255 else c
            draw.point((i, j), (a, b, c))
    noised_image_path = os.path.splitext(image_path)[0] + "_noised.jpg"
    image.save(noised_image_path, "JPEG")

    return noised_image_path

def apply_median_filter(image, window_size, direction, progressbar, func):
    """
    Применяет медианный фильтр к изображению в заданном направлении.
    """
    func(0)
    width, height = image.size
    filtered_image = Image.new("RGB", (width, height))

    if direction == 'horizontal':
        value = height//100
        val=0
        for y in range(height):
            func(val)
            val+=value
            for x in range(width):
                left = max(0, x - window_size // 2)
                right = min(width, x + window_size // 2 + 1)
                window = [image.getpixel((i, y)) for i in range(left, right)]
                window.sort(key=lambda p: p[0])
                r_median = window[len(window) // 2][0]
                window.sort(key=lambda p: p[1])
                g_median = window[len(window) // 2][1]
                window.sort(key=lambda p: p[2])
                b_median = window[len(window) // 2][2]
                filtered_image.putpixel((x, y), (r_median, g_median, b_median))
    elif direction == 'vertical':
        value = width//100
        val = value
        for x in range(width):
            for y in range(height):
                top = max(0, y - window_size // 2)
                bottom = min(height, y + window_size // 2 + 1)
                window = [image.getpixel((x, j)) for j in range(top, bottom)]
                window.sort(key=lambda p: p[0])
                r_median = window[len(window) // 2][0]
                window.sort(key=lambda p: p[1])
                g_median = window[len(window) // 2][1]
                window.sort(key=lambda p: p[2])
                b_median = window[len(window) // 2][2]
                filtered_image.putpixel((x, y), (r_median, g_median, b_median))
            func(val)
            val += value
    else:
        raise ValueError("Invalid direction parameter. Use 'horizontal' or 'vertical'.")
    func(0)
    return filtered_image

def apply_combined_median_filter(image, window_size, progressbar, func):
    """
    Применяет объединенный медианный фильтр к изображению.
    """
    width, height = image.size
    filtered_image = Image.new("RGB", (width, height))
    value = height//100
    val = 0
    func(0)
    for y in range(height):
        for x in range(width):
            left = max(0, x - window_size // 2)
            right = min(width, x + window_size // 2 + 1)
            top = max(0, y - window_size // 2)
            bottom = min(height, y + window_size // 2 + 1)

            window = []
            for j in range(top, bottom):
                for i in range(left, right):
                    window.append(image.getpixel((i, j)))

            window.sort(key=lambda p: p[0])
            r_median = window[len(window) // 2][0]
            window.sort(key=lambda p: p[1])
            g_median = window[len(window) // 2][1]
            window.sort(key=lambda p: p[2])
            b_median = window[len(window) // 2][2]

            filtered_image.putpixel((x, y), (r_median, g_median, b_median))
        val += value
        func(val)
    return filtered_image
