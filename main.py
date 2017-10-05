from skimage.io import imread
from skimage.util import random_noise
from skimage.util.shape import view_as_blocks
from skimage import img_as_ubyte
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D

import numpy as np

from aswm_ref.aswm import aswm, myfilt


from skimage.morphology import disk
from skimage.filters.rank import median

def plot(img):
    plt.figure()
    plt.imshow(img, cmap='gray', interpolation='none')

def compare(img, imgs):
    from skimage.measure import compare_psnr
    from skimage.measure import compare_ssim

    psnr = compare_psnr(img, imgs)
    ssim = compare_ssim(img, imgs)

    return psnr, ssim


from scipy.io import savemat

if __name__ == "__main__":

    psnr_aswm = []

    ssim_aswm = []



    path = "img/lena.png"
    img = imread(path, as_grey=True)
    img = img_as_ubyte(img)

    noise_levels = [0.05, 0.10, 0.15, 0.20, 0.25, 0.30, 0.35, 0.40, 0.45, 0.50, 0.55, 0.60, 0.65, 0.70, 0.75, 0.80, 0.85, 0.90]

    th_levels = range(0, 50, 5)

    ssim_my = {}
    psnr_my = {}

    for th in th_levels:
        psnr_my[th] = []
        ssim_my[th] = []


    for i in noise_levels:
        imgn = random_noise(img, mode='s&p', amount=i)

        imgs = aswm(imgn)

        ps, ss = compare(img, imgs)
        psnr_aswm.append(ps)
        ssim_aswm.append(ss)

        for th in th_levels:
            imgs2 = myfilt(imgn,  th / 50.0)

            ps, ss = compare(img, imgs2)
            psnr_my[th].append(ps)
            ssim_my[th].append(ss)


    plt.plot(noise_levels, psnr_aswm, label="ASWM")

    for th in th_levels:
        plt.plot(noise_levels, psnr_my[th], label="Our {}".format(th))


    print("psnr:")
    print("aswm:", psnr_aswm)
    for th in th_levels:
        print("our {}:".format(th), psnr_my[th])

    print("ssim:")
    print("aswm:", ssim_aswm)
    for th in th_levels:
        print("our {}:".format(th), ssim_my[th])

    plt.legend(loc='upper right')

    # psnr_my["aswm"] = psnr_aswm
    # savemat("myfilt_stats_psnr.mat", psnr_my)
    #
    # ssim_my["aswm"] = ssim_aswm
    # savemat("myfilt_stats_ssim.mat", ssim_my)


    plt.show()