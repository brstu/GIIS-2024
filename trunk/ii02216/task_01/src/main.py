from tkinter import filedialog
from tkinter import *
from PIL import Image, ImageTk
import secrets

image_path = None  # путь к выбранному изображению
noisy_image_path = None  # путь к зашумленному изображению

def load_image(image_label):
    global image_path
    image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png; *.jpg; *.jpeg")])
    show_image(image_path, image_label)

def add_impulse_noise():
    global image_path, noisy_image_path
    if image_path:
        image = Image.open(image_path)
        noise_factor = noise_slider.get() / 100.0
        noisy_image = add_impulse_noise_to_image(image, noise_factor)
        noisy_image_path = "noisy_image.jpg"
        noisy_image.save(noisy_image_path)
        show_noisy_image(noisy_image_path)

def apply_median_filter():
    global noisy_image_path
    if noisy_image_path:
        noisy_image = Image.open(noisy_image_path)
        apply_row_filter = row_checkbox_var.get() == 1
        apply_column_filter = column_checkbox_var.get() == 1
        filtered_image = apply_median_filter_to_image(noisy_image, apply_row_filter, apply_column_filter)
        show_filtered_image(filtered_image)

def show_image(image_path, image_label):
    if image_path:
        image = Image.open(image_path)
        image.thumbnail((400, 400))
        image_tk = ImageTk.PhotoImage(image)
        image_label.config(image=image_tk)
        image_label.image = image_tk

def show_noisy_image(noisy_image_path):
    if noisy_image_path:
        noisy_image = Image.open(noisy_image_path)
        noisy_image.thumbnail((400, 400))
        noisy_image_tk = ImageTk.PhotoImage(noisy_image)
        noisy_image_label.config(image=noisy_image_tk)
        noisy_image_label.image = noisy_image_tk

def show_filtered_image(filtered_image):
    if filtered_image:
        filtered_image.thumbnail((400, 400))
        filtered_image_tk = ImageTk.PhotoImage(filtered_image)
        noisy_image_label.config(image=filtered_image_tk)
        noisy_image_label.image = filtered_image_tk

def add_impulse_noise_to_image(image, noise_factor):
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

def apply_median_filter_to_image(image, apply_row_filter, apply_column_filter):
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

# Создание окна приложения с интерфейсом tkinter
root = Tk()
root.state('zoomed')
root.title("Фильтрация изображения от импульсных помех")

# Создаем два фрейма, используем grid для размещения по горизонтали
frame1 = Frame(root)
frame2 = Frame(root)

frame1.grid(row=0, column=0, sticky='nsew')
frame2.grid(row=0, column=1, sticky='nsew')

# Устанавливаем вес колонок, чтобы они распределялись в пропорции 1:2
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=2)

# Создание кнопок
load_button = Button(frame1, text="Загрузить изображение", command=lambda: load_image(image_label))
load_button.pack()

add_noise_button = Button(frame1, text="Добавить помехи", command=add_impulse_noise)
add_noise_button.pack()

apply_filter_button = Button(frame1, text="Применить медианный фильтр", command=apply_median_filter)
apply_filter_button.pack()

# Создание ползунка для выбора уровня зашумления
noise_slider = Scale(frame1, orient=HORIZONTAL, label="Уровень зашумления (%)", from_=0, to=100)
noise_slider.pack()

# Создание галочек для выбора фильтрации по строкам и по столбцам
row_checkbox_var = IntVar()
row_checkbox = Checkbutton(frame1, text="Фильтрация по строкам", variable=row_checkbox_var)
row_checkbox.pack()

column_checkbox_var = IntVar()
column_checkbox = Checkbutton(frame1, text="Фильтрация по столбцам", variable=column_checkbox_var)
column_checkbox.pack()

# Создание меток для отображения изображений
image_label = Label(frame2)
image_label.pack()

noisy_image_label = Label(frame2)
noisy_image_label.pack()

root.mainloop()
