import numpy as np

c = 3e8  ## m/s

def threeAnchorCalculate(x1, y1, x2, y2, x3, y3, TDOA21, TDOA31):
    print(x1, y1, x2, y2, x3, y3, TDOA21, TDOA31)
    p1 = np.mat([[x2 - x1, y2 - y1], [x3 - x1, y3 - y1]])
    print(p1)
    print('\n')
    p1 = -p1.I

    p2 = np.mat([[TDOA21 * c], [TDOA31 * c]])

    p3 = 1/2 * np.mat([[x1 ** 2 + y1 ** 2 - x2 ** 2 - y2 ** 2 + (TDOA21 * c) ** 2],
                [x1 ** 2 + y1 ** 2 - x3 ** 2 - y3 ** 2 + (TDOA31 * c) ** 2]])

    n1 = np.mat([[x1], [y1]])

    A = float((p1 * p2).T * (p1 * p2) - 1)
    B = float((p1 * p2).T * (p1 * p3 - n1) + (p1 * p3 - n1).T * (p1 * p2))
    C = float((p1 * p3 - n1).T * (p1 * p3 - n1))
    t = B ** 2 - 4 * A * C
    r1 = r2 = 0
    mat1 = mat2 = np.mat([[0], [0]])
    if t > 0:
        r1 = (-B + t ** 0.5) / (2 * A)
        r2 = (-B - t ** 0.5) / (2 * A)
        if r1 > 0:
            mat1 = p1 * p2 * r1 + p1 * p3
        if r2 > 0:
            mat2 = p1 * p2 * r2 + p1 * p3
    elif t == 0:
        r1 = r2 = (-B + t ** 0.5) / (2 * A)
        mat1 = mat2 = p1 * p2 * r1 + p1 * p3
    return ((r1, mat1[0, 0], mat1[1, 0]), (r2, mat2[0, 0], mat2[1, 0]))