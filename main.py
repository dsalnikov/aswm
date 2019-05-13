from skimage.io import imread, imsave
from skimage.util import random_noise
from skimage.util.shape import view_as_blocks
from skimage import img_as_ubyte
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
import csv
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
    img = imread(path, as_gray=True)
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
        
        imsave("img/out/lena_n{}.png".format(i), imgn)

        imgs = aswm(imgn)

        ps, ss = compare(img, imgs)
        psnr_aswm.append(ps)
        ssim_aswm.append(ss)
        
        imsave("img/out_aswm/lena_n{}_psnr{}_ssim{}_.png".format(i, ps, ss), imgs)

        for th in th_levels:
            imgs2 = myfilt(imgn,  th / 50.0)

            ps, ss = compare(img, imgs2)

            imsave("img/out_our/lena_n{}_th{}_psnr{}_ssim{}_.png".format(i, th, ps, ss), imgs2)

            psnr_my[th].append(ps)
            ssim_my[th].append(ss)


    plt.plot(noise_levels, psnr_aswm, label="ASWM")

    for th in th_levels:
        plt.plot(noise_levels, psnr_my[th], label="Our {}".format(th))


    header = ['noise level', 'aswm psnr', 'aswm ssim', 'aswm fix psnr', 'aswm fix ssim']

    for th in th_levels:
        header.append('our_{} psnr'.format(th))
        header.append('our_{} ssim'.format(th))

    with open('statistics.csv', 'w') as f:
        w = csv.DictWriter(f, header)

        w.writeheader()

        for i in range(0, len(noise_levels)):
            row = {}
            row["noise level"] = noise_levels[i]
            row["aswm psnr"] = psnr_aswm[i]
            row["aswm ssim"] = ssim_aswm[i]
            row["aswm fix psnr"] = psnr_aswm[i]
            row["aswm fix ssim"] = ssim_aswm[i]

            for th in th_levels:
                row['our_{} psnr'.format(th)] = psnr_my[th][i]
                row['our_{} ssim'.format(th)] = ssim_my[th][i]

            w.writerow(row)

    plt.legend(loc='upper right')

    plt.savefig("statistics.png")