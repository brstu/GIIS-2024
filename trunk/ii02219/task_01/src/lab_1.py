import tkinter as tk
from tkinter import filedialog
import cv2
import numpy as np

def open_image():
    global original_image
    file_path = filedialog.askopenfilename(title="Open Image")
    if file_path:
        original_image = cv2.imread(file_path)
        cv2.imshow("Original Image", original_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

def add_noise():
    global noisy_image
    if original_image is None:
        return
    noise_level = noise_slider.get()
    rng = np.random.default_rng(seed=12345)  # Set your seed here
    noise = rng.normal(0, noise_level, original_image.shape)
    noisy_image = original_image + noise
    noisy_image = np.clip(noisy_image, 0, 255).astype(np.uint8)
    cv2.imshow("Noisy Image", noisy_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def filter_image():
    global filtered_image
    if noisy_image is None:
        return
    threshold = threshold_slider.get()
    _, filtered_image = cv2.threshold(noisy_image, threshold, 255, cv2.THRESH_BINARY)
    cv2.imshow("Filtered Image", filtered_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

root = tk.Tk()
root.title("Image Filter Application")

original_image = None
noisy_image = None
filtered_image = None

open_button = tk.Button(root, text="Open Image", command=open_image)
open_button.pack()

noise_button = tk.Button(root, text="Add Noise", command=add_noise)
noise_button.pack()

noise_slider = tk.Scale(root, from_=0, to=100, orient="horizontal", label="Noise Level")
noise_slider.pack()

filter_button = tk.Button(root, text="Filter Image", command=filter_image)
filter_button.pack()

threshold_slider = tk.Scale(root, from_=0, to=255, orient="horizontal", label="Threshold")
threshold_slider.pack()

root.mainloop()
