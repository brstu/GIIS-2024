import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

image_paths = ["image/1.png","image/2.png","image/3.png","image/4.png","image/5.png","image/6.png","image/7.png","image/8.png","image/9.png"]

images = [Image.open(path) for path in image_paths]

fig, ax = plt.subplots()
ax.axis('off')

img = ax.imshow(images[0])

def update(frame):
    img.set_array(images[frame])
    return img,


ani = FuncAnimation(fig, update, frames=len(images), interval=95)

plt.show()
