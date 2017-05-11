from skimage.io import imread
from skimage.util import random_noise
from skimage.util.shape import view_as_blocks
from skimage import img_as_ubyte
import numpy as np


def frac_mul(a, b):
    return (a * b) >> 16

def frac_div(a, b):
    return ((a << 15) / b) << 1

def frac_sqrt(num):
    """
    fixed point sqrt rewrited from fix16_sqrt lib
    refer https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Binary_numeral_system_.28base_2.29 for more details
    """

    neg = num < 0
    num = abs(num)
    res = 0

    if num & 0xFFF00000:
        bit = 1 << 30
    else:
        bit = 1 << 18

    while bit > num:
        bit = bit >> 2

    for n in range(0, 2):
        while bit != 0:
            if num >= res + bit:
                num = num - (res + bit)
                res = (res >> 1) + bit
            else:
                res = res >> 1
            bit = bit >> 2

        if n == 0:
            if num > 65535:
                num = num - res
                num = (num << 16) - 0x8000
                res = (res << 16) + 0x8000
            else:
                num = num << 16
                res = res << 16

            bit = 1 << 14

    if neg:
        res = -res

    return res

def F16(x):
    return int(x * 65536.0)

def weighted_mean(weights, window, size):
    acc = 0
    wacc = 0

    for i in range(0, size):
        wacc = wacc + frac_mul(weights[i], window[i] << 16)
        acc = acc + weights[i]

    return frac_div(wacc, acc)

def deviation(weights, window, mean, size):
    acc = 0
    wacc = 0

    for i in range(0, size):
        diff = (window[i] << 16) - mean
        ddiff = frac_mul(diff, diff)

        wacc = wacc + frac_mul(weights[i], ddiff)
        acc = acc + weights[i]

    return frac_sqrt(frac_div(wacc, acc))

def aswm(imgn):
    img = img_as_ubyte(imgn, force_copy=True)

    cols, rows = img.shape

    for i in range(1, cols - 1):
        for j in range(1, rows - 1):
            weights = [F16(1.0), F16(1.0), F16(1.0), F16(1.0), F16(1.0), F16(1.0), F16(1.0), F16(1.0), F16(1.0)]

            window = []
            window.append(img[i - 1, j - 1])
            window.append(img[i, j - 1])
            window.append(img[i + 1, j - 1])
            window.append(img[i - 1, j])
            window.append(img[i, j])
            window.append(img[i + 1, j])
            window.append(img[i - 1, j + 1])
            window.append(img[i, j + 1])
            window.append(img[i + 1, j + 1])

            mean = weighted_mean(weights, window, 9)

            while True:

                for l in range(0, 9):
                    x = abs((window[l] << 16) - mean) + F16(0.1)
                    weights[l] = ((F16(1.0) << 16) / x) << 1

                new_mean = weighted_mean(weights, window, 9)
                diff = abs(new_mean - mean)
                mean = new_mean
                if diff < F16(0.1):
                    break

            dev = deviation(weights, window, mean, 9)

            if abs((window[4] << 16) - mean) > frac_mul(dev, F16(6.5)):
                w = sorted(window)
                img[i, j] = w[4]

    return img
