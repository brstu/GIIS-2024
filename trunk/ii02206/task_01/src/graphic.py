import tkinter as tk
from tkinter import ttk
import numpy as np
from tkinter import filedialog
from tkinter import messagebox
from PIL import Image, ImageTk
import MyLogic


class PhotoEditorApp:
    def __init__(self, master):
        self.progress_val = 0

        self.master = master
        self.master.title("Photo Editor")

        self.image_label = tk.Label(self.master)
        self.image_label.pack()

        self.progressbar = ttk.Progressbar(orient=tk.VERTICAL, length=340)
        self.progressbar.pack(side=tk.LEFT, padx=0, pady=5)

        self.button_select_photo = tk.Button(self.master, text="Выбрать фото", command=self.load_image, width=20)
        self.button_select_photo.pack(side=tk.TOP, padx=5, pady=5)

        self.separator1 = ttk.Separator(self.master, orient=tk.HORIZONTAL)
        self.separator1.pack(fill='x', pady=5)

        self.noise_label = tk.Label(self.master, text="Шум:")
        self.noise_label.pack(side=tk.TOP, padx=5, pady=5)
        self.noise_entry = tk.Entry(self.master, width=20)
        self.noise_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.noise_scale = tk.Scale(self.master, label="Шум", from_=0, to=100, orient=tk.HORIZONTAL, width=20,
                                    command=self.update_noise_scale)
        self.noise_scale.pack(side=tk.TOP, padx=5, pady=5)

        self.button_noise = tk.Button(self.master, text="Зашумить", command=self.add_noise, width=20)
        self.button_noise.pack(side=tk.TOP, padx=5, pady=5)

        self.separator2 = ttk.Separator(self.master, orient=tk.HORIZONTAL)
        self.separator2.pack(fill='x', pady=5)

        self.window_size_label = tk.Label(self.master, text="Размер окна:")
        self.window_size_label.pack(side=tk.TOP, padx=5, pady=5)
        self.window_size_entry = tk.Entry(self.master, width=20)
        self.window_size_entry.pack(side=tk.TOP, padx=5, pady=5)
        self.window_size_scale = tk.Scale(self.master, label="Размер окна", from_=3, to=151, resolution=2,
                                          orient=tk.HORIZONTAL, width=20, command=self.update_window_size_scale)
        self.window_size_scale.pack(side=tk.TOP, padx=5, pady=5)

        self.button_horizontal = tk.Button(self.master, text="Горизонтальный метод", command=self.horizontal_method,
                                           width=20)
        self.button_horizontal.pack(side=tk.TOP, padx=5, pady=5)

        self.button_vertical = tk.Button(self.master, text="Вертикальный метод", command=self.vertical_method, width=20)
        self.button_vertical.pack(side=tk.TOP, padx=5, pady=5)

        self.button_combined = tk.Button(self.master, text="Совмещённый", command=self.combined_method, width=20)
        self.button_combined.pack(side=tk.TOP, padx=5, pady=5)

        self.button_save = tk.Button(self.master, text="Сохранить фото", command=self.save_image, width=20)
        self.button_save.pack(side=tk.TOP, padx=5, pady=5)

        # Привязываем события изменения значений в полях ввода к соответствующим функциям
        self.noise_entry.bind("<Return>", self.update_noise_scale_from_entry)
        self.window_size_entry.bind("<Return>", self.update_window_size_scale_from_entry)

    def load_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Изображения", "*.jpg;*.jpeg;*.png")])
        if file_path:
            image = Image.open(file_path)
            image = image.resize((400,250))
            self.original_image = image.copy()
            photo = ImageTk.PhotoImage(image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo  # сохраняем ссылку на изображение

    def save_image(self):
        if hasattr(self, 'original_image'):
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png")])
            if file_path:
                self.original_image.save(file_path)

    def add_noise(self):
        if hasattr(self, 'original_image'):
            noisy_image = self.original_image.copy()
            width, height = noisy_image.size
            pixels = noisy_image.load()
            noise_level = int(self.noise_entry.get()) if self.noise_entry.get() else self.noise_scale.get()

            for i in range(width):
                for j in range(height):
                    r, g, b = pixels[i, j]
                    noise = np.random.randint(-noise_level, noise_level)
                    pixels[i, j] = (
                        self._clamp(r + noise),
                        self._clamp(g + noise),
                        self._clamp(b + noise)
                    )

            photo = ImageTk.PhotoImage(noisy_image)
            self.image_label.configure(image=photo)
            self.image_label.image = photo

    def update_progressbar(self, progress_value):
        self.progressbar['value'] = progress_value
        self.progressbar.update()
        # print(self.progressbar['value'])

    def horizontal_method(self):
        if hasattr(self, 'original_image'):
            window_size = int(
                self.window_size_entry.get()) if self.window_size_entry.get() else self.window_size_scale.get()
            if window_size % 2 == 1:  # Проверяем, что размер окна нечетный
                image = self.original_image.copy()
                print(window_size)
                filtered_image = MyLogic.apply_median_filter(image, window_size, 'horizontal', self.progressbar,
                                                             self.update_progressbar)
                self.display_image(filtered_image)
            else:
                messagebox.showwarning("Ошибка", "Число должно быть больше или равно 3 и нечётное")

    def vertical_method(self):
        if hasattr(self, 'original_image'):
            window_size = int(
                self.window_size_entry.get()) if self.window_size_entry.get() else self.window_size_scale.get()
            if window_size % 2 == 1:  # Проверяем, что размер окна нечетный
                image = self.original_image.copy()
                filtered_image = MyLogic.apply_median_filter(image, window_size, 'vertical', self.progressbar,
                                                             self.update_progressbar)
                self.display_image(filtered_image)
            else:
                messagebox.showwarning("Ошибка", "Число должно быть больше или равно 3 и нечётное")

    def combined_method(self):
        if hasattr(self, 'original_image'):
            window_size = int(
                self.window_size_entry.get()) if self.window_size_entry.get() else self.window_size_scale.get()
            if window_size % 2 == 1:  # Проверяем, что размер окна нечетный
                image = self.original_image.copy()
                filtered_image = MyLogic.apply_combined_median_filter(image, window_size, self.progressbar,
                                                                      self.update_progressbar)
                self.display_image(filtered_image)
            else:
                messagebox.showwarning("Ошибка", "Число должно быть больше или равно 3 и нечётное")

    def display_image(self, image):
        photo = ImageTk.PhotoImage(image)
        self.image_label.configure(image=photo)
        self.image_label.image = photo

    def show_alert():
        messagebox.showwarning("Warning", "This is a warning message!")

    def _clamp(self, value, minimum=0, maximum=255):
        return max(min(value, maximum), minimum)

    # Обновление значения ползунка шума при вводе в соответствующее поле
    def update_noise_scale_from_entry(self, event):
        try:
            new_value = int(self.noise_entry.get())
            if 0 <= new_value <= 100:
                # Устанавливаем новое значение для шума
                self.noise_scale.set(new_value)
        except ValueError:
            pass

    # Обновление значения ползунка размера окна при вводе в соответствующее поле
    def update_window_size_scale_from_entry(self, event):
        try:
            new_value = int(self.window_size_entry.get())
            if new_value % 2 == 1 and 3 <= new_value <= 151:
                # Устанавливаем новое значение для размера окна
                self.window_size_scale.set(new_value)
            else:
                messagebox.showwarning("Warning", "Window size must be an odd number between 3 and 151!")
        except ValueError:
            pass

    # Обновление значения поля ввода шума при изменении ползунка
    def update_noise_scale(self, event):
        self.noise_entry.delete(0, tk.END)
        self.noise_entry.insert(0, str(self.noise_scale.get()))

    # Обновление значения поля ввода размера окна при изменении ползунка
    def update_window_size_scale(self, event):
        self.window_size_entry.delete(0, tk.END)
        self.window_size_entry.insert(0, str(self.window_size_scale.get()))


def main():
    root = tk.Tk()
    app = PhotoEditorApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
