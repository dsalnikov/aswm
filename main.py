from skimage.io import imread
from skimage.util import random_noise
from skimage.util.shape import view_as_blocks
from skimage import img_as_ubyte
import matplotlib.pyplot as plt
import numpy as np

from aswm_ref.aswm import aswm




def plot(img):
    plt.figure()
    plt.imshow(img, cmap='gray', interpolation='none')

def compare(img, imgs):
    from skimage.measure import compare_psnr
    from skimage.measure import compare_ssim

    print("PSRN: {}".format(compare_psnr(img, imgs)))
    print("SSIM: {}".format(compare_ssim(img, imgs)))



if __name__ == "__main__":
    path = "img/lena.png"
    img = imread(path, as_grey=True)
    img = img_as_ubyte(img)
    imgn = random_noise(img, mode='s&p', amount=0.75)

    # filter image with ASWM filter
    imgs = aswm(imgn)

    plot(imgs)
    plot(imgn)

    compare(img, imgs)

    plt.show()