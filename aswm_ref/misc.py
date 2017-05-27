
def sqrt(d):

    q = 0
    r = 0

    lst = [15, 14, 13, 12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]
    for i in lst:
        if r >= 0:
            r = (r << 2) | ((d>>(i+i)) & 3)
            r = r - ((q<<2)|1)
        else:
            r = (r << 2) | ((d>>(i+i)) & 3)
            r = r + ((q<<2)|3)

        if r >= 0:
            q = (q << 1) | 1
        else:
            q = (q << 1) | 0

    if r < 0:
        r = r + ((q << 1) | 1)

    return q

if __name__ == "__main__":
    print(sqrt(9))