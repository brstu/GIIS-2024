import os
from PIL import Image

# Указываем путь к папке с изображениями
image_folder = '../Image'

frames = []

# Получаем список файлов в папке
image_files = sorted(os.listdir(image_folder))

for image_file in image_files:
    if image_file.endswith('.png'):
        # Открываем каждое изображение и добавляем его в список frames
        frame = Image.open(os.path.join(image_folder, image_file))
        # Приводим изображение к одинаковому размеру и режиму
        frame = frame.convert('RGBA').resize((1000, 800))
        frames.append(frame)

# Сохраняем GIF изображение
frames[0].save(
    'photo.gif',
    save_all=True,
    append_images=frames[1:],
    optimize=True,
    duration=100,
    loop=0
)