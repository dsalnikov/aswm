from myhdl import *
from hdl.misc import *

def Multiplier(clk, x, w, wx):

    @always(clk.posedge)
    def MultiplierLogic():
        wx.next = (w * x << 16) >> 16

    return MultiplierLogic

def Adder(clk, a, b, outp):

    @always(clk.posedge)
    def AdderLogic():
        outp.next = a + b

    return AdderLogic

def FracDiv(clk, num, den, q):

    @always(clk.posedge)
    def FracDivLogic():
        q.next = ((num << 15) // den) << 1

    return FracDivLogic

def FracDiv2(clk, num, den, q):

    @always(clk.posedge)
    def FracDiv2Logic():
        q.next = ((num << 16) // den) << 1

    return FracDiv2Logic


def WMean(clk,
          x0, x1, x2, x3, x4, x5, x6, x7, x8,
          w0, w1, w2, w3, w4, w5, w6, w7, w8,
          wmean):

    x = [x0, x1, x2, x3, x4, x5, x6, x7, x8]
    w = [w0, w1, w2, w3, w4, w5, w6, w7, w8]
    add_l_0 = [Signal(intbv(0, min=w0.min, max=w0.max)) for i in range(9)]
    add_l_1 = [Signal(intbv(0, min=w0.min, max=w0.max)) for i in range(5)]
    add_l_2 = [Signal(intbv(0, min=w0.min, max=w0.max)) for i in range(3)]
    add_l_3 = [Signal(intbv(0, min=w0.min, max=w0.max)) for i in range(2)]
    y = [Signal(intbv(0, min=x0.min, max=x0.max)) for i in range(9)]

    # multiplying each input
    mull_inst = []
    for i in range(9):
        mull_inst.append(Multiplier(clk, x[i], w[i], add_l_0[i]))

    # Calculation of weighted sum in 4clks
    wacc = Signal(intbv(0, min=w0.min, max=w0.max))

    adder_inst_0 = Adder(clk, add_l_0[0], add_l_0[1], add_l_1[0])
    adder_inst_1 = Adder(clk, add_l_0[2], add_l_0[3], add_l_1[1])
    adder_inst_2 = Adder(clk, add_l_0[4], add_l_0[5], add_l_1[2])
    adder_inst_3 = Adder(clk, add_l_0[6], add_l_0[7], add_l_1[3])

    adder_inst_4 = Adder(clk, add_l_1[0], add_l_1[1], add_l_2[0])
    adder_inst_5 = Adder(clk, add_l_1[2], add_l_1[3], add_l_2[1])

    adder_inst_6 = Adder(clk, add_l_2[0], add_l_2[1], add_l_3[0])

    adder_inst_7 = Adder(clk, add_l_3[0], add_l_3[1], wacc)

    # Registers to pipeline calculations
    reg_inst_0 = Register(clk, add_l_0[8], add_l_1[4])
    reg_inst_1 = Register(clk, add_l_1[4], add_l_2[2])
    reg_inst_2 = Register(clk, add_l_2[2], add_l_3[1])

    # Calculation of weights sum in 4clks
    # Init signals with 1 to prevent div by 0
    acc = Signal(intbv(1, min=w0.min, max=w0.max))

    wsum_l_0 = [Signal(intbv(1, min=w0.min, max=w0.max)) for i in range(5)]
    wsum_l_1 = [Signal(intbv(1, min=w0.min, max=w0.max)) for i in range(3)]
    wsum_l_2 = [Signal(intbv(1, min=w0.min, max=w0.max)) for i in range(2)]

    adder_inst_8 = Adder(clk, w[0], w[1], wsum_l_0[0])
    adder_inst_9 = Adder(clk, w[2], w[3], wsum_l_0[1])
    adder_inst_10 = Adder(clk, w[4], w[5], wsum_l_0[2])
    adder_inst_11 = Adder(clk, w[6], w[7], wsum_l_0[3])

    adder_inst_12 = Adder(clk, wsum_l_0[0], wsum_l_0[1], wsum_l_1[0])
    adder_inst_13 = Adder(clk, wsum_l_0[2], wsum_l_0[3], wsum_l_1[1])

    adder_inst_14 = Adder(clk, wsum_l_1[0], wsum_l_1[1], wsum_l_2[0])

    adder_inst_15 = Adder(clk, wsum_l_2[0], wsum_l_2[1], acc)

    # Registers to pipeline calculations
    reg_inst_3 = Register(clk, w[8], wsum_l_0[4])
    reg_inst_4 = Register(clk, wsum_l_0[4], wsum_l_1[2])
    reg_inst_5 = Register(clk, wsum_l_1[2], wsum_l_2[1])

    # Calculate weighted mean
    div_inst = FracDiv(clk, wacc, acc, wmean)

    return instances()

def WeightsEstimate(clk,
                    wmean,
                    x0, x1, x2, x3, x4, x5, x6, x7, x8,
                    w0, w1, w2, w3, w4, w5, w6, w7, w8):

    x = [x0, x1, x2, x3, x4, x5, x6, x7, x8]
    w = [w0, w1, w2, w3, w4, w5, w6, w7, w8]

    sub_0 = [Signal(modbv(0, min=w0.min, max=w0.max)) for i in range(9)]
    sub_1 = [Signal(modbv(0, min=w0.min, max=w0.max)) for i in range(9)]
    sub_2 = [Signal(modbv(0, min=w0.min, max=w0.max)) for i in range(9)]
    signs_0 = [Signal(modbv(0)) for i in range(9)]

    add_0 = [Signal(modbv(0x2000, min=w0.min, max=w0.max)) for i in range(9)]

    sub_inst = []
    for i in range(9):
       sub_inst.append(Sub2(clk, x[i], wmean, sub_0[i], sub_1[i], signs_0[i]))

    mux_inst = []
    for i in range(9):
        mux_inst.append(Mux2(clk, signs_0[i], sub_0[i], sub_1[i], sub_2[i]))

    add_const = Signal(modbv(0x1999, min=w0.min, max=w0.max))

    add_inst = []
    for i in range(9):
        add_inst.append(Adder(clk, sub_2[i], add_const, add_0[i]))

    div_num = Signal(intbv(0x10000, min=w0.min, max=w0.max))

    div_inst = []
    for i in range(9):
        div_inst.append(FracDiv2(clk, div_num, add_0[i], w[i]))


    return instances()


"""
def deviation(weights, window, mean, size):
    acc = 0
    wacc = 0

    for i in range(0, size):
        diff = (window[i] << 16) - mean
        ddiff = frac_mul(diff, diff)

        wacc = wacc + frac_mul(weights[i], ddiff)
        acc = acc + weights[i]

    return frac_sqrt(frac_div(wacc, acc))
"""



def Deviation(clk,
              w0, w1, w2, w3, w4, w5, w6, w7, w8,
              win0, win1, win2, win3, win4, win5, win6, win7, win8,
              wmean,
              deviation,
              d0, d1, d2, d3, d4, d5, d6, d7, d8):

    debug = [d0, d1, d2, d3, d4, d5, d6, d7, d8]

    win = [win0, win1, win2, win3, win4, win5, win6, win7, win8]
    w = [w0, w1, w2, w3, w4, w5, w6, w7, w8]

    diff_l_0 = [Signal(modbv(0x00020000, min=-2**32, max=2**32)) for i in range(9)]
    diff_l_1 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(9)]
    wdiff_l_0 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(9)]
    # print(win)
    diff_inst_0 = []
    for i in range(9):
        diff_inst_0.append(Diff(clk, wmean, win[i], diff_l_0[i]))

    diff_inst_1 = []
    for i in range(9):
        diff_inst_1.append(Pow2(clk, diff_l_0[i], diff_l_1[i]))


    # w pipeline for 2clks
    w_delay_l_0 = [Signal(modbv(0x00010000, min=w0.min, max=w0.max)) for i in range(9)]
    w_delay_l_1 = [Signal(modbv(0x00010000, min=w0.min, max=w0.max)) for i in range(9)]

    w_delay_regs_inst_0 = []
    for i in range(9):
        w_delay_regs_inst_0.append(Register(clk, w[i], w_delay_l_0[i]))

    w_delay_regs_inst_1 = []
    for i in range(9):
        w_delay_regs_inst_1.append(Register(clk, w_delay_l_0[i], w_delay_l_1[i]))


    wdiff_inst_0 = []
    for i in range(9):
        wdiff_inst_0.append(Mul2(clk, diff_l_1[i], w_delay_l_1[i], wdiff_l_0[i]))



    wacc = Signal(modbv(1, min=w0.min, max=w0.max))

    add_wacc_l_0 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(5)]
    add_wacc_l_1 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(3)]
    add_wacc_l_2 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(2)]

    adder_inst_0 = Adder(clk, wdiff_l_0[0], wdiff_l_0[1], add_wacc_l_0[0])
    adder_inst_1 = Adder(clk, wdiff_l_0[2], wdiff_l_0[3], add_wacc_l_0[1])
    adder_inst_2 = Adder(clk, wdiff_l_0[4], wdiff_l_0[5], add_wacc_l_0[2])
    adder_inst_3 = Adder(clk, wdiff_l_0[6], wdiff_l_0[7], add_wacc_l_0[3])

    adder_inst_4 = Adder(clk, add_wacc_l_0[0], add_wacc_l_0[1], add_wacc_l_1[0])
    adder_inst_5 = Adder(clk, add_wacc_l_0[2], add_wacc_l_0[3], add_wacc_l_1[1])

    adder_inst_6 = Adder(clk, add_wacc_l_1[0], add_wacc_l_1[1], add_wacc_l_2[0])

    adder_inst_7 = Adder(clk, add_wacc_l_2[0], add_wacc_l_2[1], wacc)

    # Registers to pipeline wacc calculation
    reg_inst_0 = Register(clk, wdiff_l_0[8], add_wacc_l_0[4])
    reg_inst_1 = Register(clk, add_wacc_l_0[4], add_wacc_l_1[2])
    reg_inst_2 = Register(clk, add_wacc_l_1[2], add_wacc_l_2[1])


    acc = Signal(intbv(1, min=w0.min, max=w0.max))

    add_acc_l_0 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(5)]
    add_acc_l_1 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(3)]
    add_acc_l_2 = [Signal(modbv(1, min=w0.min, max=w0.max)) for i in range(2)]

    add_acc_l_3 = Signal(modbv(1, min=w0.min, max=w0.max))
    add_acc_l_4 = Signal(modbv(1, min=w0.min, max=w0.max))
    add_acc_l_5 = Signal(modbv(1, min=w0.min, max=w0.max))

    adder_acc_inst_0 = Adder(clk, w[0], w[1], add_acc_l_0[0])
    adder_acc_inst_1 = Adder(clk, w[2], w[3], add_acc_l_0[1])
    adder_acc_inst_2 = Adder(clk, w[4], w[5], add_acc_l_0[2])
    adder_acc_inst_3 = Adder(clk, w[6], w[7], add_acc_l_0[3])

    adder_acc_inst_4 = Adder(clk, add_acc_l_0[0], add_acc_l_0[1], add_acc_l_1[0])
    adder_acc_inst_5 = Adder(clk, add_acc_l_0[2], add_acc_l_0[3], add_acc_l_1[1])

    adder_acc_inst_6 = Adder(clk, add_acc_l_1[0], add_acc_l_1[1], add_acc_l_2[0])

    adder_acc_inst_7 = Adder(clk, add_acc_l_2[0], add_acc_l_2[1], add_acc_l_3)


    # Registers to pipeline acc calculation
    reg_acc_inst_0 = Register(clk, w[8], add_acc_l_0[4])
    reg_acc_inst_1 = Register(clk, add_acc_l_0[4], add_acc_l_1[2])
    reg_acc_inst_2 = Register(clk, add_acc_l_1[2], add_acc_l_2[1])

    reg_acc_inst_3 = Register(clk, add_acc_l_3, add_acc_l_4)
    reg_acc_inst_4 = Register(clk, add_acc_l_4, add_acc_l_5)
    reg_acc_inst_5 = Register(clk, add_acc_l_5, acc)


    div_response = Signal(modbv(1, min=w0.min, max=w0.max))

    div_inst = FracDiv(clk, wacc, acc, div_response)
    sqrt_inst = sqrt(clk, div_response, deviation)

    return instances()