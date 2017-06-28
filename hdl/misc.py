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

def Sub(clk, a, b, q):

    @always(clk.posedge)
    def SubLogic():
        q.next = a - b

def sqrt(clk, d, q):
    """
    Pipelined SQRT implementation
    See more details here: http://cis.k.hosei.ac.jp/%7Eyamin/papers/ICCD96.pdf

    """

    msb_0 = Signal(bool(0))
    msb_0_out = Signal(intbv(0)[2:])
    res_0 = Signal(intbv(0)[2:])

    msb_1 = Signal(bool(0))
    msb_1_out = Signal(intbv(0)[3:])
    res_1 = Signal(intbv(0)[3:])

    msb_2 = Signal(bool(0))
    msb_2_out = Signal(intbv(0)[4:])
    res_2 = Signal(intbv(0)[4:])

    msb_3 = Signal(bool(0))
    msb_3_out = Signal(intbv(0)[5:])
    res_3 = Signal(intbv(0)[5:])

    msb_4 = Signal(bool(0))
    msb_4_out = Signal(intbv(0)[6:])
    res_4 = Signal(intbv(0)[6:])

    msb_5 = Signal(bool(0))
    msb_5_out = Signal(intbv(0)[7:])
    res_5 = Signal(intbv(0)[7:])

    msb_6 = Signal(bool(0))
    msb_6_out = Signal(intbv(0)[8:])
    res_6 = Signal(intbv(0)[8:])

    msb_7 = Signal(bool(0))
    msb_7_out = Signal(intbv(0)[9:])
    res_7 = Signal(intbv(0)[9:])

    msb_8 = Signal(bool(0))
    msb_8_out = Signal(intbv(0)[10:])
    res_8 = Signal(intbv(0)[10:])

    msb_9 = Signal(bool(0))
    msb_9_out = Signal(intbv(0)[11:])
    res_9 = Signal(intbv(0)[11:])

    msb_10 = Signal(bool(0))
    msb_10_out = Signal(intbv(0)[12:])
    res_10 = Signal(intbv(0)[12:])

    msb_11 = Signal(bool(0))
    msb_11_out = Signal(intbv(0)[13:])
    res_11 = Signal(intbv(0)[13:])

    msb_12 = Signal(bool(0))
    msb_12_out = Signal(intbv(0)[14:])
    res_12 = Signal(intbv(0)[14:])

    msb_13 = Signal(bool(0))
    msb_13_out = Signal(intbv(0)[15:])
    res_13 = Signal(intbv(0)[15:])

    msb_14 = Signal(bool(0))
    msb_14_out = Signal(intbv(0)[16:])
    res_14 = Signal(intbv(0)[16:])

    d_pipe = [Signal(intbv(0)[32:]) for i in range(16)]

    @always(clk.posedge)
    def d_pipe_stage():
        d_pipe[14].next = d
        for i in range(0, 14):
            d_pipe[i].next = d_pipe[i+1]

    @always_comb
    #@always(clk.posedge)
    def stage_result():
        q.next = msb_14_out

    @always(clk.posedge)
    def stage_0():
        res = modbv(0, min=-2**2, max=2**2)
        res[:] = d[32:30] - 1
        msb_0.next = not res[2]
        res_0.next = res[2:0]

    @always(clk.posedge)
    def stage_1():
        sum_a = intbv(0)[4:]
        sum_a[2:0] = d_pipe[14][30:28]
        sum_a[4:2] = res_0

        sum_b = intbv(0)[4:]
        sum_b[3] = 0
        sum_b[2] = msb_0
        sum_b[1] = not msb_0
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**3, max=2**3)

        if msb_0 == 0:
            sum_res[:] = sum_a + sum_b

            msb_1.next = not sum_res[3]
            res_1.next = sum_res[3:0]

            msb_0_out.next[0] = not sum_res[3]
            msb_0_out.next[1] = msb_0
        else:
            sum_res[:] = sum_a - sum_b

            msb_1.next = not sum_res[3]
            res_1.next = sum_res[3:0]

            msb_0_out.next[0] = not sum_res[3]
            msb_0_out.next[1] = msb_0

    @always(clk.posedge)
    def stage_2():
        sum_a = intbv(0)[5:]
        sum_a[2:0] = d_pipe[13][28:26]
        sum_a[5:2] = res_1

        sum_b = intbv(0)[5:]
        sum_b[4] = 0
        sum_b[4:2] = msb_0_out
        sum_b[1] = not msb_1
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**4, max=2**4)

        if msb_1 == 0:
            sum_res[:] = sum_a + sum_b

            msb_2.next = not sum_res[4]
            res_2.next = sum_res[4:0]

            msb_1_out.next[3:1] = msb_0_out
            msb_1_out.next[0] = not sum_res[4]
        else:
            sum_res[:] = sum_a - sum_b

            msb_2.next = not sum_res[4]
            res_2.next = sum_res[4:0]

            msb_1_out.next[3:1] = msb_0_out
            msb_1_out.next[0] = not sum_res[4]

    @always(clk.posedge)
    def stage_3():
        sum_a = intbv(0)[6:]
        sum_a[2:0] = d_pipe[12][26:24]
        sum_a[6:2] = res_2

        sum_b = intbv(0)[6:]
        sum_b[5] = 0
        sum_b[5:2] = msb_1_out
        sum_b[1] = not msb_2
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**5, max=2**5)

        if msb_2 == 0:
            sum_res[:] = sum_a + sum_b

            msb_3.next = not sum_res[5]
            res_3.next = sum_res[5:0]

            msb_2_out.next[4:1] = msb_1_out
            msb_2_out.next[0] = not sum_res[5]
        else:
            sum_res[:] = sum_a - sum_b

            msb_3.next = not sum_res[5]
            res_3.next = sum_res[5:0]

            msb_2_out.next[4:1] = msb_1_out
            msb_2_out.next[0] = not sum_res[5]

    @always(clk.posedge)
    def stage_4():
        sum_a = intbv(0)[7:]
        sum_a[2:0] = d_pipe[11][24:22]
        sum_a[7:2] = res_3

        sum_b = intbv(0)[7:]
        sum_b[6] = 0
        sum_b[6:2] = msb_2_out
        sum_b[1] = not msb_3
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**6, max=2**6)

        if msb_3 == 0:
            sum_res[:] = sum_a + sum_b

            msb_4.next = not sum_res[6]
            res_4.next = sum_res[6:0]

            msb_3_out.next[5:1] = msb_2_out
            msb_3_out.next[0] = not sum_res[6]
        else:
            sum_res[:] = sum_a - sum_b

            msb_4.next = not sum_res[6]
            res_4.next = sum_res[6:0]

            msb_3_out.next[5:1] = msb_2_out
            msb_3_out.next[0] = not sum_res[6]

    @always(clk.posedge)
    def stage_5():
        sum_a = intbv(0)[8:]
        sum_a[2:0] = d_pipe[10][22:20]
        sum_a[8:2] = res_4

        sum_b = intbv(0)[8:]
        sum_b[7] = 0
        sum_b[7:2] = msb_3_out
        sum_b[1] = not msb_4
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**7, max=2**7)

        if msb_4 == 0:
            sum_res[:] = sum_a + sum_b

            msb_5.next = not sum_res[7]
            res_5.next = sum_res[7:0]

            msb_4_out.next[6:1] = msb_3_out
            msb_4_out.next[0] = not sum_res[7]
        else:
            sum_res[:] = sum_a - sum_b

            msb_5.next = not sum_res[7]
            res_5.next = sum_res[7:0]

            msb_4_out.next[6:1] = msb_3_out
            msb_4_out.next[0] = not sum_res[7]

    @always(clk.posedge)
    def stage_6():
        sum_a = intbv(0)[9:]
        sum_a[2:0] = d_pipe[9][20:18]
        sum_a[9:2] = res_5

        sum_b = intbv(0)[9:]
        sum_b[8] = 0
        sum_b[8:2] = msb_4_out
        sum_b[1] = not msb_5
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**8, max=2**8)

        if msb_5 == 0:
            sum_res[:] = sum_a + sum_b

            msb_6.next = not sum_res[8]
            res_6.next = sum_res[8:0]

            msb_5_out.next[7:1] = msb_4_out
            msb_5_out.next[0] = not sum_res[8]
        else:
            sum_res[:] = sum_a - sum_b

            msb_6.next = not sum_res[8]
            res_6.next = sum_res[8:0]

            msb_5_out.next[7:1] = msb_4_out
            msb_5_out.next[0] = not sum_res[8]

    @always(clk.posedge)
    def stage_7():
        sum_a = intbv(0)[10:]
        sum_a[2:0] = d_pipe[8][18:16]
        sum_a[10:2] = res_6

        sum_b = intbv(0)[10:]
        sum_b[9] = 0
        sum_b[9:2] = msb_5_out
        sum_b[1] = not msb_6
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**9, max=2**9)

        if msb_6 == 0:
            sum_res[:] = sum_a + sum_b

            msb_7.next = not sum_res[9]
            res_7.next = sum_res[9:0]

            msb_6_out.next[8:1] = msb_5_out
            msb_6_out.next[0] = not sum_res[9]
        else:
            sum_res[:] = sum_a - sum_b

            msb_7.next = not sum_res[9]
            res_7.next = sum_res[9:0]

            msb_6_out.next[8:1] = msb_5_out
            msb_6_out.next[0] = not sum_res[9]

    @always(clk.posedge)
    def stage_8():
        sum_a = intbv(0)[11:]
        sum_a[2:0] = d_pipe[7][16:14]
        sum_a[11:2] = res_7

        sum_b = intbv(0)[11:]
        sum_b[10] = 0
        sum_b[10:2] = msb_6_out
        sum_b[1] = not msb_7
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**10, max=2**10)

        if msb_7 == 0:
            sum_res[:] = sum_a + sum_b

            msb_8.next = not sum_res[10]
            res_8.next = sum_res[10:0]

            msb_7_out.next[9:1] = msb_6_out
            msb_7_out.next[0] = not sum_res[10]
        else:
            sum_res[:] = sum_a - sum_b

            msb_8.next = not sum_res[10]
            res_8.next = sum_res[10:0]

            msb_7_out.next[9:1] = msb_6_out
            msb_7_out.next[0] = not sum_res[10]

    @always(clk.posedge)
    def stage_9():
        sum_a = intbv(0)[12:]
        sum_a[2:0] = d_pipe[6][14:12]
        sum_a[12:2] = res_8

        sum_b = intbv(0)[12:]
        sum_b[11] = 0
        sum_b[10] = msb_0
        sum_b[11:2] = msb_7_out
        sum_b[1] = not msb_8
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**11, max=2**11)

        if msb_8 == 0:
            sum_res[:] = sum_a + sum_b

            msb_9.next = not sum_res[11]
            res_9.next = sum_res[11:0]

            msb_8_out.next[10:1] = msb_7_out
            msb_8_out.next[0] = not sum_res[11]
        else:
            sum_res[:] = sum_a - sum_b

            msb_9.next = not sum_res[11]
            res_9.next = sum_res[11:0]

            msb_8_out.next[10:1] = msb_7_out
            msb_8_out.next[0] = not sum_res[11]


    @always(clk.posedge)
    def stage_10():
        sum_a = intbv(0)[13:]
        sum_a[2:0] = d_pipe[5][12:10]
        sum_a[13:2] = res_9

        sum_b = intbv(0)[13:]
        sum_b[12] = 0
        sum_b[12:2] = msb_8_out
        sum_b[1] = not msb_9
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**12, max=2**12)

        if msb_9 == 0:
            sum_res[:] = sum_a + sum_b

            msb_10.next = not sum_res[12]
            res_10.next = sum_res[12:0]

            msb_9_out.next[11:1] = msb_8_out
            msb_9_out.next[0] = not sum_res[12]
        else:
            sum_res[:] = sum_a - sum_b

            msb_10.next = not sum_res[12]
            res_10.next = sum_res[12:0]

            msb_9_out.next[11:1] = msb_8_out
            msb_9_out.next[0] = not sum_res[12]

    @always(clk.posedge)
    def stage_11():
        sum_a = intbv(0)[14:]
        sum_a[2:0] = d_pipe[4][10:8]
        sum_a[14:2] = res_10

        sum_b = intbv(0)[14:]
        sum_b[13] = 0
        sum_b[13:2] = msb_9_out
        sum_b[1] = not msb_10
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**13, max=2**13)

        if msb_10 == 0:
            sum_res[:] = sum_a + sum_b

            msb_11.next = not sum_res[13]
            res_11.next = sum_res[13:0]

            msb_10_out.next[12:1] = msb_9_out
            msb_10_out.next[0] = not sum_res[13]
        else:
            sum_res[:] = sum_a - sum_b

            msb_11.next = not sum_res[13]
            res_11.next = sum_res[13:0]

            msb_10_out.next[12:1] = msb_9_out
            msb_10_out.next[0] = not sum_res[13]

    @always(clk.posedge)
    def stage_12():
        sum_a = intbv(0)[15:]
        sum_a[2:0] = d_pipe[3][8:6]
        sum_a[15:2] = res_11

        sum_b = intbv(0)[15:]
        sum_b[14] = 0
        sum_b[14:2] = msb_10_out
        sum_b[1] = not msb_11
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**14, max=2**14)

        if msb_11 == 0:
            sum_res[:] = sum_a + sum_b

            msb_12.next = not sum_res[14]
            res_12.next = sum_res[14:0]

            msb_11_out.next[13:1] = msb_10_out
            msb_11_out.next[0] = not sum_res[14]

        else:
            sum_res[:] = sum_a - sum_b

            msb_12.next = not sum_res[14]
            res_12.next = sum_res[14:0]

            msb_11_out.next[13:1] = msb_10_out
            msb_11_out.next[0] = not sum_res[14]

    @always(clk.posedge)
    def stage_13():
        sum_a = intbv(0)[16:]
        sum_a[2:0] = d_pipe[2][6:4]
        sum_a[16:2] = res_12

        sum_b = intbv(0)[16:]
        sum_b[15] = 0
        sum_b[15:2] = msb_11_out
        sum_b[1] = not msb_12
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**15, max=2**15)

        if msb_12 == 0:
            sum_res[:] = sum_a + sum_b

            msb_13.next = not sum_res[15]
            res_13.next = sum_res[15:0]

            msb_12_out.next[14:1] = msb_11_out
            msb_12_out.next[0] = not sum_res[15]
        else:
            sum_res[:] = sum_a - sum_b

            msb_13.next = not sum_res[15]
            res_13.next = sum_res[15:0]

            msb_12_out.next[14:1] = msb_11_out
            msb_12_out.next[0] = not sum_res[15]


    @always(clk.posedge)
    def stage_14():
        sum_a = intbv(0)[17:]
        sum_a[2:0] = d_pipe[1][4:2]
        sum_a[17:2] = res_13

        sum_b = intbv(0)[17:]
        sum_b[16] = 0
        sum_b[16:2] = msb_12_out
        sum_b[1] = not msb_13
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**16, max=2**16)

        if msb_13 == 0:
            sum_res[:] = sum_a + sum_b

            msb_14.next = not sum_res[16]
            res_14.next = sum_res[16:0]

            msb_13_out.next[15:1] = msb_12_out
            msb_13_out.next[0] = not sum_res[16]
        else:
            sum_res[:] = sum_a - sum_b

            msb_14.next = not sum_res[16]
            res_14.next = sum_res[16:0]

            msb_13_out.next[15:1] = msb_12_out
            msb_13_out.next[0] = not sum_res[16]

    @always(clk.posedge)
    def stage_15():
        sum_a = intbv(0)[18:]
        sum_a[2:0] = d_pipe[0][4:2]
        sum_a[18:2] = res_14

        sum_b = intbv(0)[18:]
        sum_b[17] = 0
        sum_b[17:2] = msb_13_out
        sum_b[1] = not msb_14
        sum_b[0] = 1

        sum_res = modbv(0, min=-2**17, max=2**17)

        if msb_14 == 0:
            sum_res[:] = sum_a + sum_b

            msb_14_out.next[16:1] = msb_13_out
            msb_14_out.next[0] = not sum_res[17]
        else:
            sum_res[:] = sum_a - sum_b

            msb_14_out.next[16:1] = msb_13_out
            msb_14_out.next[0] = not sum_res[17]

    return instances()


if __name__ == "__main__":
    clk = Signal(bool(0))
    a = Signal(intbv(0)[32:])
    b = Signal(intbv(0)[16:])
    inst = toVHDL(sqrt, clk, a, b)