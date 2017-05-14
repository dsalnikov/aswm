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

def sqrt(clk, d, q):
    """
    Pipelined SQRT implementation
    See more details here: http://cis.k.hosei.ac.jp/%7Eyamin/papers/ICCD96.pdf

    """

    msb_0 = Signal(bool(0))
    res_0 = Signal(intbv(0)[2:])

    msb_1 = Signal(bool(0))
    res_1 = Signal(intbv(0)[3:])

    msb_2 = Signal(bool(0))
    res_2 = Signal(intbv(0)[4:])

    msb_3 = Signal(bool(0))
    res_3 = Signal(intbv(0)[5:])

    msb_4 = Signal(bool(0))
    res_4 = Signal(intbv(0)[6:])

    msb_5 = Signal(bool(0))
    res_5 = Signal(intbv(0)[7:])

    msb_6 = Signal(bool(0))
    res_6 = Signal(intbv(0)[8:])

    msb_7 = Signal(bool(0))
    res_7 = Signal(intbv(0)[9:])

    msb_8 = Signal(bool(0))
    res_8 = Signal(intbv(0)[10:])

    msb_9 = Signal(bool(0))
    res_9 = Signal(intbv(0)[11:])

    msb_10 = Signal(bool(0))
    res_10 = Signal(intbv(0)[12:])

    msb_11 = Signal(bool(0))
    res_11 = Signal(intbv(0)[13:])

    msb_12 = Signal(bool(0))
    res_12 = Signal(intbv(0)[14:])

    msb_13 = Signal(bool(0))
    res_13 = Signal(intbv(0)[15:])

    msb_14 = Signal(bool(0))
    res_14 = Signal(intbv(0)[16:])

    msb_15 = Signal(bool(0))
    res_15 = Signal(intbv(0)[17:])

    res_d = Signal(intbv(0)[4:])


    @always_comb
    def stage_result():
        # TODO: change separate signals to registers
        q.next[15] = msb_0
        q.next[14] = msb_1
        q.next[13] = msb_2
        q.next[12] = msb_3
        q.next[11] = msb_4
        q.next[10] = msb_5
        q.next[9] = msb_6
        q.next[8] = msb_7
        q.next[7] = msb_8
        q.next[6] = msb_9
        q.next[5] = msb_10
        q.next[4] = msb_11
        q.next[3] = msb_12
        q.next[2] = msb_13
        q.next[1] = msb_14
        q.next[0] = msb_15

    @always(clk.posedge)
    def stage_0():
        res = intbv(d[32:30] - 1)[3:]
        msb_0.next = not res[2]
        res_0.next = res[2:0]

    @always(clk.posedge)
    def stage_1():
        sum_a = intbv(0)[4:]
        sum_a[2:0] = d[30:28]
        sum_a[4:2] = res_0

        sum_b = intbv(0)[4:]
        sum_b[3] = 0
        sum_b[2] = msb_0
        sum_b[1] = not msb_0
        sum_b[0] = 1

        if msb_0 == 0:
            sum_res = intbv(sum_a + sum_b)[4:]

            msb_1.next = not sum_res[3]
            res_1.next = sum_res[3:0]
        else:
            sum_res = intbv(sum_a - sum_b)[4:]

            msb_1.next = not sum_res[3]
            res_1.next = sum_res[3:0]

    @always(clk.posedge)
    def stage_2():
        sum_a = intbv(0)[5:]
        sum_a[2:0] = d[28:26]
        sum_a[5:2] = res_1

        sum_b = intbv(0)[5:]
        sum_b[4] = 0
        sum_b[3] = msb_0
        sum_b[2] = msb_1
        sum_b[1] = not msb_1
        sum_b[0] = 1

        if msb_1 == 0:
            sum_res = intbv(sum_a + sum_b)[5:]

            msb_2.next = not sum_res[4]
            res_2.next = sum_res[4:0]
        else:
            sum_res = intbv(sum_a - sum_b)[5:]

            msb_2.next = not sum_res[4]
            res_2.next = sum_res[4:0]

    @always(clk.posedge)
    def stage_3():
        sum_a = intbv(0)[6:]
        sum_a[2:0] = d[26:24]
        sum_a[6:2] = res_2

        sum_b = intbv(0)[6:]
        sum_b[5] = 0
        sum_b[4] = msb_0
        sum_b[3] = msb_1
        sum_b[2] = msb_2
        sum_b[1] = not msb_2
        sum_b[0] = 1

        if msb_2 == 0:
            sum_res = intbv(sum_a + sum_b)[6:]

            msb_3.next = not sum_res[5]
            res_3.next = sum_res[5:0]
        else:
            sum_res = intbv(sum_a - sum_b)[6:]

            msb_3.next = not sum_res[5]
            res_3.next = sum_res[5:0]

    @always(clk.posedge)
    def stage_4():
        sum_a = intbv(0)[7:]
        sum_a[2:0] = d[24:22]
        sum_a[7:2] = res_3

        sum_b = intbv(0)[7:]
        sum_b[6] = 0
        sum_b[5] = msb_0
        sum_b[4] = msb_1
        sum_b[3] = msb_2
        sum_b[2] = msb_3
        sum_b[1] = not msb_3
        sum_b[0] = 1

        if msb_3 == 0:
            sum_res = intbv(sum_a + sum_b)[7:]

            msb_4.next = not sum_res[6]
            res_4.next = sum_res[6:0]
        else:
            sum_res = intbv(sum_a - sum_b)[7:]

            msb_4.next = not sum_res[6]
            res_4.next = sum_res[6:0]

    @always(clk.posedge)
    def stage_5():
        sum_a = intbv(0)[8:]
        sum_a[2:0] = d[22:20]
        sum_a[8:2] = res_4

        sum_b = intbv(0)[8:]
        sum_b[7] = 0
        sum_b[6] = msb_0
        sum_b[5] = msb_1
        sum_b[4] = msb_2
        sum_b[3] = msb_3
        sum_b[2] = msb_4
        sum_b[1] = not msb_4
        sum_b[0] = 1

        if msb_4 == 0:
            sum_res = intbv(sum_a + sum_b)[8:]

            msb_5.next = not sum_res[7]
            res_5.next = sum_res[7:0]
        else:
            sum_res = intbv(sum_a - sum_b)[8:]

            msb_5.next = not sum_res[7]
            res_5.next = sum_res[7:0]

    @always(clk.posedge)
    def stage_6():
        sum_a = intbv(0)[9:]
        sum_a[2:0] = d[20:18]
        sum_a[9:2] = res_5

        sum_b = intbv(0)[9:]
        sum_b[8] = 0
        sum_b[7] = msb_0
        sum_b[6] = msb_1
        sum_b[5] = msb_2
        sum_b[4] = msb_3
        sum_b[3] = msb_4
        sum_b[2] = msb_5
        sum_b[1] = not msb_5
        sum_b[0] = 1

        if msb_5 == 0:
            sum_res = intbv(sum_a + sum_b)[9:]

            msb_6.next = not sum_res[8]
            res_6.next = sum_res[8:0]
        else:
            sum_res = intbv(sum_a - sum_b)[9:]

            msb_6.next = not sum_res[8]
            res_6.next = sum_res[8:0]

    @always(clk.posedge)
    def stage_7():
        sum_a = intbv(0)[10:]
        sum_a[2:0] = d[18:16]
        sum_a[10:2] = res_6

        sum_b = intbv(0)[10:]
        sum_b[9] = 0
        sum_b[8] = msb_0
        sum_b[7] = msb_1
        sum_b[6] = msb_2
        sum_b[5] = msb_3
        sum_b[4] = msb_4
        sum_b[3] = msb_5
        sum_b[2] = msb_6
        sum_b[1] = not msb_6
        sum_b[0] = 1

        if msb_6 == 0:
            sum_res = intbv(sum_a + sum_b)[10:]

            msb_7.next = not sum_res[9]
            res_7.next = sum_res[9:0]
        else:
            sum_res = intbv(sum_a - sum_b)[10:]

            msb_7.next = not sum_res[9]
            res_7.next = sum_res[9:0]

    @always(clk.posedge)
    def stage_8():
        sum_a = intbv(0)[11:]
        sum_a[2:0] = d[16:14]
        sum_a[11:2] = res_7

        sum_b = intbv(0)[11:]
        sum_b[10] = 0
        sum_b[9] = msb_0
        sum_b[8] = msb_1
        sum_b[7] = msb_2
        sum_b[6] = msb_3
        sum_b[5] = msb_4
        sum_b[4] = msb_5
        sum_b[3] = msb_6
        sum_b[2] = msb_7
        sum_b[1] = not msb_7
        sum_b[0] = 1

        if msb_7 == 0:
            sum_res = intbv(sum_a + sum_b)[11:]

            msb_8.next = not sum_res[10]
            res_8.next = sum_res[10:0]
        else:
            sum_res = intbv(sum_a - sum_b)[11:]

            msb_8.next = not sum_res[10]
            res_8.next = sum_res[10:0]

    @always(clk.posedge)
    def stage_9():
        sum_a = intbv(0)[12:]
        sum_a[2:0] = d[14:12]
        sum_a[12:2] = res_8

        sum_b = intbv(0)[12:]
        sum_b[11] = 0
        sum_b[10] = msb_0
        sum_b[9] = msb_1
        sum_b[8] = msb_2
        sum_b[7] = msb_3
        sum_b[6] = msb_4
        sum_b[5] = msb_5
        sum_b[4] = msb_6
        sum_b[3] = msb_7
        sum_b[2] = msb_8
        sum_b[1] = not msb_8
        sum_b[0] = 1

        if msb_8 == 0:
            sum_res = intbv(sum_a + sum_b)[12:]

            msb_9.next = not sum_res[11]
            res_9.next = sum_res[11:0]
        else:
            sum_res = intbv(sum_a - sum_b)[12:]

            msb_9.next = not sum_res[11]
            res_9.next = sum_res[11:0]

    @always(clk.posedge)
    def stage_10():
        sum_a = intbv(0)[13:]
        sum_a[2:0] = d[12:10]
        sum_a[13:2] = res_9

        sum_b = intbv(0)[13:]
        sum_b[12] = 0
        sum_b[11] = msb_0
        sum_b[10] = msb_1
        sum_b[9] = msb_2
        sum_b[8] = msb_3
        sum_b[7] = msb_4
        sum_b[6] = msb_5
        sum_b[5] = msb_6
        sum_b[4] = msb_7
        sum_b[3] = msb_8
        sum_b[2] = msb_9
        sum_b[1] = not msb_9
        sum_b[0] = 1

        if msb_9 == 0:
            sum_res = intbv(sum_a + sum_b)[13:]

            msb_10.next = not sum_res[12]
            res_10.next = sum_res[12:0]
        else:
            sum_res = intbv(sum_a - sum_b)[13:]

            msb_10.next = not sum_res[12]
            res_10.next = sum_res[12:0]

    @always(clk.posedge)
    def stage_11():
        sum_a = intbv(0)[14:]
        sum_a[2:0] = d[10:8]
        sum_a[14:2] = res_10

        sum_b = intbv(0)[14:]
        sum_b[13] = 0
        sum_b[12] = msb_0
        sum_b[11] = msb_1
        sum_b[10] = msb_2
        sum_b[9] = msb_3
        sum_b[8] = msb_4
        sum_b[7] = msb_5
        sum_b[6] = msb_6
        sum_b[5] = msb_7
        sum_b[4] = msb_8
        sum_b[3] = msb_9
        sum_b[2] = msb_10
        sum_b[1] = not msb_10
        sum_b[0] = 1

        if msb_10 == 0:
            sum_res = intbv(sum_a + sum_b)[14:]

            msb_11.next = not sum_res[13]
            res_11.next = sum_res[13:0]
        else:
            sum_res = intbv(sum_a - sum_b)[14:]

            msb_11.next = not sum_res[13]
            res_11.next = sum_res[13:0]

    @always(clk.posedge)
    def stage_12():
        sum_a = intbv(0)[15:]
        sum_a[2:0] = d[8:6]
        sum_a[15:2] = res_11

        sum_b = intbv(0)[15:]
        sum_b[14] = 0
        sum_b[13] = msb_0
        sum_b[12] = msb_1
        sum_b[11] = msb_2
        sum_b[10] = msb_3
        sum_b[9] = msb_4
        sum_b[8] = msb_5
        sum_b[7] = msb_6
        sum_b[6] = msb_7
        sum_b[5] = msb_8
        sum_b[4] = msb_9
        sum_b[3] = msb_10
        sum_b[2] = msb_11
        sum_b[1] = not msb_11
        sum_b[0] = 1

        if msb_11 == 0:
            sum_res = intbv(sum_a + sum_b)[15:]

            msb_12.next = not sum_res[14]
            res_12.next = sum_res[14:0]
        else:
            sum_res = intbv(sum_a - sum_b)[15:]

            msb_12.next = not sum_res[14]
            res_12.next = sum_res[14:0]

    @always(clk.posedge)
    def stage_13():
        sum_a = intbv(0)[16:]
        sum_a[2:0] = d[6:4]
        sum_a[16:2] = res_12

        sum_b = intbv(0)[16:]
        sum_b[15] = 0
        sum_b[14] = msb_0
        sum_b[13] = msb_1
        sum_b[12] = msb_2
        sum_b[11] = msb_3
        sum_b[10] = msb_4
        sum_b[9] = msb_5
        sum_b[8] = msb_6
        sum_b[7] = msb_7
        sum_b[6] = msb_8
        sum_b[5] = msb_9
        sum_b[4] = msb_10
        sum_b[3] = msb_11
        sum_b[2] = msb_12
        sum_b[1] = not msb_12
        sum_b[0] = 1

        if msb_12 == 0:
            sum_res = intbv(sum_a + sum_b)[16:]

            msb_13.next = not sum_res[15]
            res_13.next = sum_res[15:0]
        else:
            sum_res = intbv(sum_a - sum_b)[16:]

            msb_13.next = not sum_res[15]
            res_13.next = sum_res[15:0]

    @always(clk.posedge)
    def stage_14():
        sum_a = intbv(0)[17:]
        sum_a[2:0] = d[4:2]
        sum_a[17:2] = res_13

        sum_b = intbv(0)[17:]
        sum_b[16] = 0
        sum_b[15] = msb_0
        sum_b[14] = msb_1
        sum_b[13] = msb_2
        sum_b[12] = msb_3
        sum_b[11] = msb_4
        sum_b[10] = msb_5
        sum_b[9] = msb_6
        sum_b[8] = msb_7
        sum_b[7] = msb_8
        sum_b[6] = msb_9
        sum_b[5] = msb_10
        sum_b[4] = msb_11
        sum_b[3] = msb_12
        sum_b[2] = msb_13
        sum_b[1] = not msb_13
        sum_b[0] = 1

        if msb_13 == 0:
            sum_res = intbv(sum_a + sum_b)[17:]

            msb_14.next = not sum_res[16]
            res_14.next = sum_res[16:0]
        else:
            sum_res = intbv(sum_a - sum_b)[17:]

            msb_14.next = not sum_res[16]
            res_14.next = sum_res[16:0]

    @always(clk.posedge)
    def stage_15():
        sum_a = intbv(0)[18:]
        sum_a[2:0] = d[4:2]
        sum_a[18:2] = res_14

        sum_b = intbv(0)[18:]
        sum_b[17] = 0
        sum_b[16] = msb_0
        sum_b[15] = msb_1
        sum_b[14] = msb_2
        sum_b[13] = msb_3
        sum_b[12] = msb_4
        sum_b[11] = msb_5
        sum_b[10] = msb_6
        sum_b[9] = msb_7
        sum_b[8] = msb_8
        sum_b[7] = msb_9
        sum_b[6] = msb_10
        sum_b[5] = msb_11
        sum_b[4] = msb_12
        sum_b[3] = msb_13
        sum_b[2] = msb_14
        sum_b[1] = not msb_14
        sum_b[0] = 1

        if msb_14 == 0:
            sum_res = intbv(sum_a + sum_b)[18:]

            msb_15.next = not sum_res[17]
            res_15.next = sum_res[17:0]
        else:
            sum_res = intbv(sum_a - sum_b)[18:]

            msb_15.next = not sum_res[17]
            res_15.next = sum_res[17:0]

    return instances()


if __name__ == "__main__":
    clk = Signal(bool(0))
    a = Signal(intbv(0)[31:])
    b = Signal(intbv(0)[16:])
    inst = toVHDL(sqrt, clk, a, b)