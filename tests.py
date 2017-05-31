from skimage.io import imread
from skimage.util import random_noise
from skimage import img_as_ubyte

from myhdl import *

from aswm_ref.aswm_fix import weighted_mean
from aswm_ref.misc import sqrt as sqrt_ref
from hdl.aswm import WMean
from hdl.misc import sqrt

from random import randint

def wmean_testbench():
    path = "img/lena.png"
    img = imread(path, as_grey=True)
    imgn = random_noise(img, mode='s&p', amount=0.75)
    img = img_as_ubyte(imgn)

    clock = Signal(bool(0))

    x = [Signal(intbv(0, min=0, max=2**8)) for _ in range(9)]
    w = [Signal(intbv(0x00010000, min=0, max=2**32)) for _ in range(9)]
    wmean = Signal(intbv(0, min=0, max=2**32))

    cmp_1 = WMean(clock, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],
                  w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8],
                  wmean)

    half_period = delay(10)

    cols, rows = img.shape

    ref_wmean = []
    win = [i for i in range(9)]

    @always(half_period)
    def clock_gen():
        clock.next = not clock

    @instance
    def stimulus():
        yield clock.posedge

        for i in range(1, cols-1):
            for j in range(1, rows-1):

                yield clock.posedge

                x[0].next = int(img[i - 1, j - 1])
                x[1].next = int(img[i, j - 1])
                x[2].next = int(img[i + 1, j - 1])
                x[3].next = int(img[i - 1, j])
                x[4].next = int(img[i, j])
                x[5].next = int(img[i + 1, j])
                x[6].next = int(img[i - 1, j + 1])
                x[7].next = int(img[i, j + 1])
                x[8].next = int(img[i + 1, j + 1])

                # save reference results
                win[0] = int(img[i - 1, j - 1])
                win[1] = int(img[i, j - 1])
                win[2] = int(img[i + 1, j - 1])
                win[3] = int(img[i - 1, j])
                win[4] = int(img[i, j])
                win[5] = int(img[i + 1, j])
                win[6] = int(img[i - 1, j + 1])
                win[7] = int(img[i, j + 1])
                win[8] = int(img[i + 1, j + 1])

                weights = [0x00010000, 0x00010000, 0x00010000,
                           0x00010000, 0x00010000, 0x00010000,
                           0x00010000, 0x00010000, 0x00010000]
                ref_res = weighted_mean(weights, win, 9)
                ref_wmean.append(ref_res)

        # wait for pipeline emptying
        for i in range(0, 8):
            yield clock.posedge

        raise StopSimulation

    @instance
    def monitor():
        # wait for pipeline filling
        for i in range(0, 8):
            yield clock.posedge

        for i in range(1, cols - 1):
            for j in range(1, rows - 1):
                yield clock.posedge

                # get reference
                ref = ref_wmean.pop(0)

                assert ref == wmean, "ref != wnean"

    return clock_gen, stimulus, cmp_1, monitor


def sqrt_testbench():
    clock = Signal(bool(0))
    a = Signal(intbv(0, min=0, max=2**32))
    b = Signal(intbv(0, min=0, max=2**16))

    sqrt_inst = sqrt(clock, a, b)

    half_period = delay(10)

    ref_wmean = []

    @always(half_period)
    def clock_gen():
        clock.next = not clock

    @instance
    def stimulus():
        for i in range(0, 1000):
            yield clock.posedge

            val =  randint(0, 2**32)

            a.next = val

            ref_res = sqrt_ref(val)
            ref_wmean.append(ref_res)

        # wait for pipeline emptying
        for i in range(0, 17):
            yield clock.posedge

        raise StopSimulation

    @instance
    def monitor():
        # wait for pipeline filling
        for i in range(0, 17):
            yield clock.posedge

        for i in range(0, 1000):
            yield clock.posedge

            ref = ref_wmean.pop(0)

            assert ref == b, "ref != hdl sqrt"

    return clock_gen, stimulus, sqrt_inst, monitor


if __name__ == "__main__":
    print("testing sqrt ...")
    sqrt_tb = sqrt_testbench()
    Simulation(sqrt_tb).run()

    print("testing wmean ...")
    wmean_tb = wmean_testbench()
    Simulation(wmean_tb).run()
