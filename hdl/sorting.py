from myhdl import *
from hdl.misc import Register

BathersNetStructure = [
    [[0, 8], [1, 5], [2, 6], [3, 7]],
    [[0, 4], [1, 3], [5, 7]],
    [[4, 8], [0, 2], [3, 5]],
    [[4, 6], [2, 8], [0, 1]],
    [[2, 4], [6, 8]],
    [[2, 3], [4, 5], [6, 7], [1, 8]],
    [[1, 4], [3, 6], [5, 8]],
    [[1, 2], [3, 4], [5, 6], [7, 8]],
]


def Swap(clk, x, y, a, b):
    return CompareExchange(clk, x[a], x[b], y[a], y[b])

def BathersNetwork(clk,
                   x0, x1, x2, x3, x4, x5, x6, x7, x8,
                   y0, y1, y2, y3, y4, y5, y6, y7, y8):

    inp = [x0, x1, x2, x3, x4, x5, x6, x7, x8]
    outp = [y0, y1, y2, y3, y4, y5, y6, y7, y8]

    # prepare interconnect signals
    x_s1 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]
    x_s2 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]
    x_s3 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]
    x_s4 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]
    x_s5 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]
    x_s6 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]
    x_s7 = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]

    signals = [inp, x_s1, x_s2, x_s3, x_s4, x_s5, x_s6, x_s7, outp]

    # construct Bather's 9 el network
    cmp_inst = []
    for stage in range(len(BathersNetStructure)):
        x = signals[stage]
        y = signals[stage + 1]
        for c in BathersNetStructure[stage]:
            cmp_inst.append(Swap(clk, x, y, c[0], c[1]))

    # append registers for pipelining
    reg_inst = []
    for stage in range(len(BathersNetStructure)):
        x = signals[stage]
        y = signals[stage + 1]
        used_lines = sum(BathersNetStructure[stage], [])

        for n in range(9):
            if n not in used_lines:
                reg_inst.append(Register(clk, x[n], y[n]))

    return instances()

def CompareExchange(clk, a, b, min, max):
    """
    Compare-exchange element
    :param clk: clock for module
    :param a: input a
    :param b: input b
    :param min: minimum element
    :param max: maximum element
    """
    @always(clk.posedge)
    def CompareExchangeLogic():
        if a > b:
            min.next = b
            max.next = a
        else:
            min.next = a
            max.next = b

    return CompareExchangeLogic
