from skimage.io import imread
from skimage.util import random_noise
from skimage.util.shape import view_as_blocks
from skimage import img_as_ubyte
import numpy as np


def weighted_mean(weights, window, size):
    acc = 0
    wacc = 0

    for i in range(0, size):
        wacc = wacc + weights[i] * window[i]
        acc = acc + weights[i]

    return wacc / acc

def deviation(weights, window, mean, size):
    import math

    acc = 0
    wacc = 0

    for i in range(0, size):
        wacc = wacc + weights[i] * math.pow(window[i] - mean, 2)
        acc = acc + weights[i]

    return math.sqrt(wacc / acc)

def aswm(imgn):
    img = img_as_ubyte(imgn, force_copy=True)

    cols, rows = img.shape

    for i in range(1, cols - 1):
        for j in range(1, rows - 1):
            weights = [1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0, 1.0]

            window = img[i - 1:i + 2, j - 1:j + 2].reshape(-1).tolist()

            mean = weighted_mean(weights, window, 9)

            while True:

                for l in range(0, 9):
                    x = abs(window[l] - mean) + 0.1
                    weights[l] = 1.0 / x

                new_mean = weighted_mean(weights, window, 9)
                diff = abs(new_mean - mean)
                mean = new_mean
                if diff < 0.1:
                    break

            dev = deviation(weights, window, mean, 9)

            if abs(window[4] - mean) > dev * 6.5:
                w = sorted(window)
                img[i, j] = w[4]

    return img
