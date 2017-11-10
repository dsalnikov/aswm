from myhdl import *
from hdl.sorting import BathersNetwork
from hdl.misc import Register


def OurFilter(clk, x0, x1, x2, x3, x4, x5, x6, x7, x8, y4):
    regs_inst = []
    y = [Signal(intbv(0)[8:]) for _ in range(9)]
    pipe_0 = [Signal(intbv(0)[8:]) for _ in range(9)]

    net_inst = BathersNetwork(clk, x0, x1, x2, x3, x4, x5, x6, x7, x8,
                              y[0], y[1], y[2], y[3], y[4], y[5], y[6], y[7], y[8])

    regs_inst.append(Register(clk, x4, pipe_0[8]))
    for i in range(0, 8):
        regs_inst.append(Register(clk, pipe_0[i+1], pipe_0[i]))


    @always(clk.posedge)
    def CMP_LOGIC():
        if y[4] - pipe_0[0] > 30:
            y4.next = y[4]
        else:
            y4.next = pipe_0[0]

    return instances()


if __name__ == "__main__":
    clk = Signal(bool(0))

    x = [Signal(intbv(0, min=0, max=2**8)) for _ in range(9)]
    y = Signal(modbv(0)[8:])

    inst = toVHDL(OurFilter,
                  clk,
                  x[0], x[1], x[2], x[3], x[4], x[5], x[6], x[7], x[8],
                  y)
