
import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import secrets

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

        self.add_noise_button = tk.Button(self.frame1, text="Добавить помехи", command=self.add_impulse_noise)
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
        self.image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png; *.jpg; *.jpeg")])
        self.show_image(self.image_path, self.image_label)

    def add_impulse_noise(self):
        if self.image_path:
            image = Image.open(self.image_path)
            noise_factor = self.noise_slider.get() / 100.0
            noisy_image = self.add_impulse_noise_to_image(image, noise_factor)
            self.noisy_image_path = "noisy_image.jpg"
            noisy_image.save(self.noisy_image_path)
            self.show_image(self.noisy_image_path, self.noisy_image_label)

    def apply_median_filter(self):
        if self.noisy_image_path:
            noisy_image = Image.open(self.noisy_image_path)
            apply_row_filter = self.row_checkbox_var.get() == 1
            apply_column_filter = self.column_checkbox_var.get() == 1
            filtered_image = self.apply_median_filter_to_image(noisy_image, apply_row_filter, apply_column_filter)
            self.show_image(filtered_image, self.noisy_image_label)

    def show_image(self, image_path, image_label):
        if image_path:
            image = Image.open(image_path)
            image.thumbnail((400, 400))
            image_tk = ImageTk.PhotoImage(image)
            image_label.config(image=image_tk)
            image_label.image = image_tk

    def add_impulse_noise_to_image(self, image, noise_factor):
        noisy_image = image.copy()
        width, height = noisy_image.size
        pixel_data = noisy_image.load()

        for i in range(width):
            for j in range(height):
                if secrets.choice([True, False]):
                    if secrets.choice([True, False]):
                        pixel_data[i, j] = (0, 0, 0)
                    else:
                        pixel_data[i, j] = (255, 255, 255)
        return noisy_image

    def apply_median_filter_to_image(self, image, apply_row_filter, apply_column_filter):
        width, height = image.size
        pixel_data = image.load()

        if apply_column_filter and apply_row_filter:
            for i in range(width):
                for j in range(height):
                    neighbors = []
                    for x in range(max(0, i - 1), min(width, i + 2)):
                        for y in range(max(0, j - 1), min(height, j + 2)):
                            neighbors.append(pixel_data[x, y])
                    neighbors.sort()
                    median_value = neighbors[len(neighbors) // 2]
                    pixel_data[i, j] = median_value
        elif apply_column_filter:
            for i in range(width):
                for j in range(height):
                    if j > 0 and j < height - 1:
                        neighbors = [
                            pixel_data[i, j - 1],
                            pixel_data[i, j],
                            pixel_data[i, j + 1]
                        ]
                        neighbors.sort()
                        median_value = neighbors[1]
                        pixel_data[i, j] = median_value
        elif apply_row_filter:
            for i in range(width):
                for j in range(height):
                    if i > 0 and i < width - 1:
                        neighbors = [
                            pixel_data[i - 1, j],
                            pixel_data[i, j],
                            pixel_data[i + 1, j]
                        ]
                        neighbors.sort()
                        median_value = neighbors[1]
                        pixel_data[i, j] = median_value

        return image


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageFilterApp(root)
    root.mainloop()
