from myhdl import Signal, always, intbv, instances, delay, Simulation, instance, StopSimulation

from hdl.misc import Register

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
