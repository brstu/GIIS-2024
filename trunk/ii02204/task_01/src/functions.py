import cv2
import numpy as np


def add_noise(image, intensity=0.02):
    noisy_image = np.copy(image)
    rng = np.random.default_rng()

    num_salt = np.ceil(intensity * image.size * 0.5)
    num_pepper = np.ceil(intensity * image.size * 0.5)

    salt_coords = [rng.integers(0, i - 1, int(num_salt)) for i in image.shape]
    noisy_image[salt_coords[0], salt_coords[1]] = 255

    pepper_coords = [rng.integers(0, i - 1, int(num_pepper)) for i in image.shape]
    noisy_image[pepper_coords[0], pepper_coords[1]] = 0

    return noisy_image


if __name__ == '__main__':
    image = cv2.imread(r'D:\PyCharm project\GIIS\lab1\img\photo.jpg', cv2.IMREAD_GRAYSCALE)

    noisy_image = add_noise(image, intensity=0.05)

    cv2.imshow('Original Image', image)
    cv2.imshow('Noisy Image', noisy_image)
    cv2.imwrite(r'D:\PyCharm project\GIIS\lab1\img\noise.jpg', noisy_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == '__main__':
    image = cv2.imread(r'D:\PyCharm project\GIIS\lab1\img\noise.jpg', cv2.IMREAD_GRAYSCALE)

    window_size = 5
    center_x = 3
    center_y = 2

    cv2.imshow('Original Image', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
