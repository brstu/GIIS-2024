import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import random
import math


class ImageProcessingApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processing App")

        self.original_image = None

        self.create_widgets()

    def create_widgets(self):
        # Menu
        menubar = tk.Menu(self.root)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self.root.quit)
        menubar.add_cascade(label="File", menu=filemenu)
        self.root.config(menu=menubar)

        # Image display
        self.canvas = tk.Canvas(self.root, width=400, height=400)
        self.canvas.pack()

        # Noise level
        self.noise_label = tk.Label(self.root, text="Noise Level: 0 %")
        self.noise_label.pack()
        self.noise_scale = tk.Scale(self.root, from_=0, to=100, orient=tk.HORIZONTAL)
        self.noise_scale.pack()

        # Generate noise button
        self.generate_noise_button = tk.Button(self.root, text="Generate Noise", command=self.generate_noise)
        self.generate_noise_button.pack()

        # Filter threshold
        self.threshold_label = tk.Label(self.root, text="Filter Threshold: 0")
        self.threshold_label.pack()
        self.threshold_scale = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL)
        self.threshold_scale.pack()

        # Apply filter button
        self.apply_filter_button = tk.Button(self.root, text="Apply Filter", command=self.apply_filter)
        self.apply_filter_button.pack()

    def open_image(self):
        filename = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg")])
        if filename:
            self.original_image = Image.open(filename)
            self.display_image(self.original_image)

    def display_image(self, image):
        self.image = ImageTk.PhotoImage(image)
        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.image)

    def generate_noise(self):
        if self.original_image:
            noise_level = self.noise_scale.get() / 100
            width, height = self.original_image.size
            pixels = self.original_image.load()
            for i in range(int(width * height * noise_level)):
                x = secrets.randbelow(width)
                y =secrets.randbelow(height)
                color = secrets.choice([0, 255])  # 0 for black, 255 for white
                pixels[x, y] = (color, color, color)
            self.display_image(self.original_image)

    def apply_filter(self):
        if self.original_image:
            threshold = self.threshold_scale.get()
            width, height = self.original_image.size
            pixels = self.original_image.load()
            for y in range(height):
                for x in range(width):
                    pixel = pixels[x, y]
                    average_intensity = self.calculate_average_intensity(pixels, x, y, width, height)
                    if abs(sum(pixel) / 3 - average_intensity) > threshold:
                        pixels[x, y] = (average_intensity, average_intensity, average_intensity)
            self.display_image(self.original_image)

    def calculate_average_intensity(self, pixels, x, y, width, height):
        sum_intensity = 0
        count = 0
        for j in range(-1, 2):
            for i in range(-1, 2):
                new_x = x + i
                new_y = y + j
                if 0 <= new_x < width and 0 <= new_y < height:
                    intensity = sum(pixels[new_x, new_y]) / 3
                    sum_intensity += intensity
                    count += 1
        return math.floor(sum_intensity / count)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageProcessingApp(root)
    root.mainloop()
