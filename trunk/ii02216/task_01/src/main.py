import tkinter as tk
from tkinter import filedialog
import cv2
from PIL import Image, ImageTk
import secrets
import numpy as np


class ImageFilterApp:
    def __init__(self, root):
        self.root = root
        self.root.state('zoomed')
        self.root.title("Фильтрация изображения от импульсных помех")

        self.frame1 = tk.Frame(root)
        self.frame2 = tk.Frame(root)

        self.frame1.grid(row=0, column=0, sticky='nsew')
        self.frame2.grid(row=0, column=1, sticky='nsew')

        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=2)

        self.image_path = None
        self.noisy_image_path = None

        self.load_button = tk.Button(self.frame1, text="Загрузить изображение", command=self.load_image)
        self.load_button.pack()

        self.add_noise_button = tk.Button(self.frame1, text="Добавить помехи", command=self.add_noise)
        self.add_noise_button.pack()

        self.apply_filter_button = tk.Button(self.frame1, text="Применить медианный фильтр", command=self.apply_median_filter)
        self.apply_filter_button.pack()

        self.noise_slider = tk.Scale(self.frame1, orient=tk.HORIZONTAL, label="Уровень зашумления (%)", from_=0, to=100)
        self.noise_slider.pack()

        self.row_checkbox_var = tk.IntVar()
        self.row_checkbox = tk.Checkbutton(self.frame1, text="Фильтрация по строкам", variable=self.row_checkbox_var)
        self.row_checkbox.pack()

        self.column_checkbox_var = tk.IntVar()
        self.column_checkbox = tk.Checkbutton(self.frame1, text="Фильтрация по столбцам", variable=self.column_checkbox_var)
        self.column_checkbox.pack()

        self.image_label = tk.Label(self.frame2)
        self.image_label.pack()

        self.noisy_image_label = tk.Label(self.frame2)
        self.noisy_image_label.pack()

    def load_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=(("Изображения", "*.jpg;*.jpeg;*.png"), ("Все файлы", "*.*")))
        if self.image_path:
            image = cv2.imread(self.image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (400, 300))
            image = Image.fromarray(image)
            image = ImageTk.PhotoImage(image)
            self.image_label.config(image=image)
            self.image_label.image = image

    def add_noise(self):
        if not self.image_path:
            return

        noise_level = self.noise_slider.get()
        if noise_level == 0:
            return

        image = cv2.imread(self.image_path)
        noisy_image = self.add_salt_and_pepper_noise(image, noise_level)
        self.noisy_image_path = "noisy_image.jpg"
        cv2.imwrite(self.noisy_image_path, noisy_image)

        noisy_image = cv2.cvtColor(noisy_image, cv2.COLOR_BGR2RGB)
        noisy_image = cv2.resize(noisy_image, (400, 300))
        noisy_image = Image.fromarray(noisy_image)
        noisy_image = ImageTk.PhotoImage(noisy_image)
        self.noisy_image_label.config(image=noisy_image)
        self.noisy_image_label.image = noisy_image

    def apply_median_filter(self):
        if not self.noisy_image_path:
            return

        noisy_image = cv2.imread(self.noisy_image_path)
        filtered_image = self.apply_median_filter_to_image(noisy_image)

        filtered_image = cv2.cvtColor(filtered_image, cv2.COLOR_BGR2RGB)
        filtered_image = cv2.resize(filtered_image, (400, 300))
        filtered_image = Image.fromarray(filtered_image)
        filtered_image = ImageTk.PhotoImage(filtered_image)

        self.noisy_image_label.config(image=filtered_image)
        self.noisy_image_label.image = filtered_image

    @staticmethod
    def add_salt_and_pepper_noise(image, noise_level):
        noisy_image = np.copy(image)
        height, width, _ = noisy_image.shape

        num_pixels = int(noise_level / 100 * height * width)
        for _ in range(num_pixels):
            x = secrets.randbelow(width)
            y = secrets.randbelow(height)
            color = secrets.choice([0, 255])
            noisy_image[y, x, :] = [color, color, color]

        return noisy_image

    @staticmethod
    def apply_median_filter_to_image(image):
        filtered_image = cv2.medianBlur(image, 3)
        return filtered_image


root = tk.Tk()
app = ImageFilterApp(root)
root.mainloop()
