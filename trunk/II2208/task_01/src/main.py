import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
import random
from copy import copy


def make_noisy(img, p):
    noisy = img
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            r = random.random()
            if r < p / 2:
                noisy[i][j] = [0, 0, 0]
            elif r < p:
                noisy[i][j] = [255, 255, 255]
            else:
                noisy[i][j] = img[i][j]
    return noisy


def median_blur(noisy_img, p):

    def median_blur_gray(noisy_img, p):
        h, w = noisy_img.shape
        pad = p // 2
        padded_image = np.pad(noisy_img, pad, mode='constant', constant_values=0)
        result = np.zeros_like(noisy_img)
        for i in range(h):
            for j in range(w):
                window = padded_image[i:i + p, j:j + p]
                median_value = np.median(window)
                result[i, j] = median_value
        return result

    if len(noisy_img.shape) == 2:
        return median_blur_gray(noisy_img, p)
    else:
        r, g, b = cv2.split(noisy_img)
        r = median_blur_gray(r, p)
        g = median_blur_gray(g, p)
        b = median_blur_gray(b, p)
        img = cv2.merge([r, g, b])
        return img


class ImageViewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Viewer")

        self.image_label = tk.Label(root)
        self.image_label.pack(pady=5)

        self.load_button = tk.Button(root, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack(pady=5)

        self.reset_button = tk.Button(root, text="Вернуть исходное изображение", command=self.apply_reset)
        self.reset_button.pack(pady=5)

        self.noise_button = tk.Button(root, text="Применить шум", command=self.apply_noise)
        self.noise_button.pack(pady=5)

        self.filter_size_label = tk.Label(root, text="Размер матрицы медианного фильтра:")
        self.filter_size_label.pack(pady=5)

        self.filter_size_entry = tk.Entry(root)
        self.filter_size_entry.pack(pady=5)

        self.median_filter_button = tk.Button(root, text="Применить медианный фильтр", command=self.apply_median_filter)
        self.median_filter_button.pack(pady=5)

        self.original_image = None
        self.noise_image = None

    def load_image(self):
        initial_dir = "./asstets"
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            self.original_image = cv2.resize(cv2.imread(file_path), (500, 500))
            self.noise_image = copy(self.original_image)
            self.display_image(self.original_image)

    def apply_median_filter(self):
        if self.original_image is not None:
            filter_size = int(self.filter_size_entry.get())
            self.noise_image = median_blur(self.noise_image, filter_size)
            self.display_image(self.noise_image)

    def apply_noise(self):
        if self.original_image is not None:
            self.noise_image = make_noisy(self.noise_image, 0.05)
            self.display_image(self.noise_image)

    def apply_reset(self):
        if self.original_image is not None:
            self.noise_image = copy(self.original_image)
            self.display_image(self.noise_image)

    def display_image(self, image):
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image_pil = Image.fromarray(image_rgb)
        photo = ImageTk.PhotoImage(image_pil)
        self.image_label.config(image=photo)
        self.image_label.image = photo


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageViewerApp(root)
    root.mainloop()
