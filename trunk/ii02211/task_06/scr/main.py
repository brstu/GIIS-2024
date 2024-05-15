import cv2
import os

path_to_images = 'C:\\Users\\VKN\\AppData\\Local\\Programs\\Python\\giis\\lab6\\img'

frames_list = []

images_files = sorted(os.listdir(path_to_images))

# Проход по каждому файлу в папке
for img_file in images_files:
    if img_file.endswith('.png'):
        frame = cv2.imread(os.path.join(path_to_images, img_file))
        frame = cv2.resize(frame, (1000, 800))
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        frames_list.append(frame)

# Сохранение GIF-изображения
cv2.imwrite('smoke_guy.gif', frames_list[0], params=[cv2.IMWRITE_PNG_COMPRESSION, 0])

# Добавление остальных кадров
for frame in frames_list[1:]:
    cv2.imwrite('smoke_guy.gif', frame, params=[cv2.IMWRITE_PNG_COMPRESSION, 0], append=True)
