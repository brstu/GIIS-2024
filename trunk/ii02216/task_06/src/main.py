import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from PIL import Image

image_paths = ["1.png","2.png","3.png","4.png","5.png","6.png","7.png","8.png","9.png"]

images = [Image.open(path) for path in image_paths]

fig, ax = plt.subplots()
ax.axis('off')


img = ax.imshow(images[0])


def update(frame):
    img.set_array(images[frame])
    return img,

ani = FuncAnimation(fig, update, frames=len(images), interval=95)

plt.show()
