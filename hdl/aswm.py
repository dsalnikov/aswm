from myhdl import Signal, always, intbv, instances, delay, Simulation, instance, StopSimulation


def Multiplier(clk, x, w, wx):

    @always(clk.posedge)
    def MultiplierLogic():
        wx.next = (w * x) >> 16

    return MultiplierLogic

def Adder(clk, a, b, outp):

    @always(clk.posedge)
    def AdderLogic():
        outp.next = a + b

    return AdderLogic

#TODO: create separete utils module
def Register(clk, inp, outp):
    """
    Syncronic register
    :param clk: clock
    :param inp: input
    :param outp: output
    """

    @always(clk.posedge)
    def RegisterLogic():
        outp.next = inp

    return RegisterLogic

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
        mull_inst.append(Multiplier(clk, x[i] << 16, w[i], add_l_0[i]))


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


def wmean_testbench():
    clock = Signal(bool(0))

    x = [i for i in range(9)]
    x[0] = Signal(intbv(0x39, min=0, max=2**8))
    x[1] = Signal(intbv(0x45, min=0, max=2**8))
    x[2] = Signal(intbv(0x3c, min=0, max=2**8))
    x[3] = Signal(intbv(0x00, min=0, max=2**8))
    x[4] = Signal(intbv(0x83, min=0, max=2**8))
    x[5] = Signal(intbv(0x00, min=0, max=2**8))
    x[6] = Signal(intbv(0x60, min=0, max=2**8))
    x[7] = Signal(intbv(0x86, min=0, max=2**8))
    x[8] = Signal(intbv(0x00, min=0, max=2**8))

    w = [Signal(intbv(0x00010000, min=0, max=2**32)) for i in range(9)]
    wmean = Signal(intbv(0, min=0, max=2**32))

    cmp_1 = WMean(clock, x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],
                  w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8],
                  wmean)

    HALF_PERIOD = delay(10)

    @always(HALF_PERIOD)
    def clockGen():
        clock.next = not clock

    @instance
    def stimulus():
        # wait for pipeline
        for i in range(8):
            yield clock.posedge

        raise StopSimulation

    @instance
    def monitor():

        # wait for pipeline
        for i in range(6):
            yield clock.posedge

        yield clock.posedge
        assert(wmean == 0x3cc71c), "Error weighted mean calculation"


    return clockGen, stimulus, cmp_1, monitor


if __name__ == "__main__":
    from myhdl import traceSignals

    #tb = traceSignals(testbench)
    tb = wmean_testbench()
    Simulation(tb).run()

    #print(wmean)

    # cmp_1 = toVHDL(WMean, clock,
    #                x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],
    #                w[0], w[1], w[2], w[3], w[4], w[5], w[6], w[7], w[8],
    #                wmean)

    # a = Signal(intbv(0, min=0, max=2**16))
    # b = Signal(intbv(0, min=0, max=2**16))
    # res = Signal(intbv(0, min=0, max=2**16))
    #
    # cmp_2 = toVHDL(FracDiv, clock, a, b, res)