from myhdl import *

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


def addsub(clk, add, a, b, q):

    @always(clk.posedge)
    def addsub_logic():
        if add == 1:
            q.next = a + b
        else:
            q.next = a - b

    return addsub_logic

def sqrt_stage(clk, a, b, add, msb, r):
    res = Signal(intbv(0, min=0, max=a.max))
    add_sub_inst_0 = addsub(clk, add, a, b, res)


    @always_comb
    def logic():
        msb.next = res[len(res)-1]
        r.next = res[len(res)-1:]

    return instances()

def sqrt(clk, d, q):
    """
    Pipelined SQRT implementation
    See more details here: http://cis.k.hosei.ac.jp/%7Eyamin/papers/ICCD96.pdf

    """

    msb = Signal(bool(0))
    r = Signal(intbv(0)[2:])
    one = Signal(intbv("001"))
    add = Signal(bool(0))

    st_inst_0 = sqrt_stage(clk, d[31:29], one, add, msb, r)
    q.next = r
    return instances()


if __name__ == "__main__":
    clk = Signal(bool(0))
    a = Signal(intbv(0)[3:])
    b = Signal(intbv(0)[3:])
    add = Signal(bool(0))
    msb = Signal(bool(0))
    r = Signal(intbv(0)[2:])
    inst = toVHDL(sqrt_stage, clk, a, b, add, msb, r)