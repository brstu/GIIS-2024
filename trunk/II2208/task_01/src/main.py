import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import numpy as np
import secrets
from copy import copy


def make_noisy(img, p):
    noisy = img
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            r = secrets.randbelow(100) / 100
            if r < p / 2:
                noisy[i][j] = [0, 0, 0]
            elif r < p:
                noisy[i][j] = [255, 255, 255]
            else:
                noisy[i][j] = img[i][j]
    return noisy


def median_blur(img, row, column, n):
    print(row, column)

    def row_median_blur(img):
        h, w = img.shape
        pad = n // 2
        padded_image = np.pad(img, pad, mode='constant', constant_values=0)
        result = np.zeros_like(img)
        for i in range(h):
            for j in range(w):
                window = padded_image[i + pad:i + n + pad, j]
                median_value = np.median(window)
                result[i, j] = median_value
        return result

    def column_median_blur(img):
        h, w = img.shape
        pad = n // 2
        padded_image = np.pad(img, pad, mode='constant', constant_values=0)
        result = np.zeros_like(img)
        for i in range(h):
            for j in range(w):
                window = padded_image[i, j + pad:j + n + pad]
                median_value = np.median(window)
                result[i, j] = median_value
        return result

    result = np.copy(img)
    if row:
        r, g, b = cv2.split(result)
        r = row_median_blur(r)
        g = row_median_blur(g)
        b = row_median_blur(b)
        result = cv2.merge([r, g, b])

    if column:
        r, g, b = cv2.split(result)
        r = column_median_blur(r)
        g = column_median_blur(g)
        b = column_median_blur(b)
        result = cv2.merge([r, g, b])

    return result


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

        self.filter_size_label = tk.Label(root, text="Размер медианного фильтра:")
        self.filter_size_label.pack(pady=5)

        self.filter_size_entry = tk.Entry(root)
        self.filter_size_entry.pack(pady=5)

        checkbox_var1 = tk.IntVar()
        checkbox_var2 = tk.IntVar()

        checkbox1 = tk.Checkbutton(root, text="по рядам", variable=checkbox_var1, onvalue=1, offvalue=0,
                                   command=self.on_checkbox_clicked1)
        checkbox2 = tk.Checkbutton(root, text="по колонкам", variable=checkbox_var2, onvalue=1, offvalue=0,
                                   command=self.on_checkbox_clicked2)
        checkbox1.pack()
        checkbox2.pack()

        self.median_filter_button = tk.Button(root, text="Применить медианный фильтр", command=self.apply_median_filter)
        self.median_filter_button.pack(pady=5)

        self.original_image = None
        self.noise_image = None
        self.row = False
        self.column = False

    def on_checkbox_clicked1(self):
        self.row = not self.row

    def on_checkbox_clicked2(self):
        self.column = not self.column

    def load_image(self):
        initial_dir = "./assets"
        file_path = filedialog.askopenfilename(initialdir=initial_dir, filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.gif;*.bmp")])

        if file_path:
            self.original_image = cv2.resize(cv2.imread(file_path), (500, 500))
            self.noise_image = copy(self.original_image)
            self.display_image(self.original_image)

    def apply_median_filter(self):
        if self.original_image is not None:
            filter_size = int(self.filter_size_entry.get())
            self.noise_image = median_blur(self.noise_image, self.row, self.column, filter_size)
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
