import math
import numpy as np

c = 299792458  ## m/s

# 三网关定位
def threeAnchorCalculate(x1, y1, x2, y2, x3, y3, t1, t2, t3):
    (dx1, dy1, dd1) = baseFourAnchorCalculate(x1, y1, x2, y2, x3, y3, t1, t2, t3)
    (dx2, dy2, dd2) = baseFourAnchorCalculate(x2, y2, x1, y1, x3, y3, t2, t1, t3)
    (dx3, dy3, dd3) = baseFourAnchorCalculate(x3, y3, x1, y1, x2, y2, t3, t1, t2)
    return ((dx1 + dx2 + dx3) / 3, (dy1 + dy2 + dy3) / 3)


def baseThreeAnchorCalculate(x1, y1, x2, y2, x3, y3, t1, t2, t3):
    D21 = (t2 - t1) * c
    D31 = (t3 - t1) * c
    p1 = np.mat([[x2 - x1, y2 - y1], [x3 - x1, y3 - y1]])
    p1 = -p1.I

    p2 = np.mat([[D21], [D31]])

    p3 = 1/2 * np.mat([[x1 ** 2 + y1 ** 2 - x2 ** 2 - y2 ** 2 + D21 ** 2],
                [x1 ** 2 + y1 ** 2 - x3 ** 2 - y3 ** 2 + D31 ** 2]])

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

# 四网关线性定位
def fourAnchorCalculate(x1, y1, x2, y2, x3, y3, x4, y4, t1, t2, t3, t4):
    (dx1, dy1, dd1) = baseFourAnchorCalculate(x1, y1, x2, y2, x3, y3, x4, y4, t1, t2, t3, t4)
    (dx2, dy2, dd2) = baseFourAnchorCalculate(x2, y2, x1, y1, x3, y3, x4, y4, t2, t1, t3, t4)
    (dx3, dy3, dd3) = baseFourAnchorCalculate(x3, y3, x1, y1, x2, y2, x4, y4, t3, t1, t2, t4)
    (dx4, dy4, dd4) = baseFourAnchorCalculate(x4, y4, x1, y1, x2, y2, x3, y3, t4, t1, t2, t3)
    return ((dx1 + dx2 + dx3 + dx4) / 4, (dy1 + dy2 + dy3 + dy4) / 4)


def baseFourAnchorCalculate(x1, y1, x2, y2, x3, y3, x4, y4, t1, t2, t3, t4):
    D21 = (t2 - t1) * c
    D31 = (t3 - t1) * c
    D41 = (t4 - t1) * c
    left = np.mat([[-2 * (x2 - x1), -2 * (y2 - y1), -2 * D21],
                 [-2 * (x3 - x1), -2 * (y3 - y1), -2 * D31],
                 [-2 * (x4 - x1), -2 * (y4 - y1), -2 * D41]])
    right = np.mat([[-pow(x2, 2) - pow(y2, 2) + pow(D21, 2) + pow(x1, 2) + pow(y1, 2)],
                    [-pow(x3, 2) - pow(y3, 2) + pow(D31, 2) + pow(x1, 2) + pow(y1, 2)],
                    [-pow(x4, 2) - pow(y4, 2) + pow(D41, 2) + pow(x1, 2) + pow(y1, 2)]])
    (dx, dy, dd) = left.I * right
    return (dx, dy ,dd)


# 四网关非线性定位
def iterativeAlgorithm(lng1, lat1, lng2, lat2, lng3, lat3, lng4, lat4, t1, t2, t3, t4):
    (dlng1, dlat1, de1) = baseFourAnchorCalculate(lng1, lat1, lng2, lat2, lng3, lat3, lng4, lat4, t1, t2, t3, t4)
    (dlng2, dlat2, de2) = baseFourAnchorCalculate(lng2, lat2, lng1, lat1, lng3, lat3, lng4, lat4, t2, t1, t3, t4)
    (dlng3, dlat3, de3) = baseFourAnchorCalculate(lng3, lat3, lng1, lat1, lng2, lat2, lng4, lat4, t3, t1, t2, t4)
    (dlng4, dlat4, de4) = baseFourAnchorCalculate(lng4, lat4, lng1, lat1, lng2, lat2, lng3, lat3, t4, t1, t2, t3)
    opt_lng = 0
    opt_lat = 0
    min_e = de1
    if de2 < min_e:
        min_e = de2
        opt_lng = dlng2
        opt_lat = dlat2
    if de3 < min_e:
        min_e = de3
        opt_lng = dlng3
        opt_lat = dlat3
    if de4 < min_e:
        min_e = de4
        opt_lng = dlng4
        opt_lat = dlat4
    return (opt_lng, opt_lat)


def haversine(lng1, lat1, lng2, lat2):
    a = 6378137                # m
    b = 6.356752314245179e+06  # m
    p = math.pi / 180          # Pi/180
    lng1 = lng1 * p
    lat1 = lat1 * p
    lng2 = lng2 * p
    lat2 = lat2 * p
    R = math.sqrt((pow(pow(a, 2) * math.cos(lat1), 2) + pow(pow(b, 2) * math.sin(lat1), 2)) / (pow(a * math.cos(lat1), 2) + pow(b * math.sin(lat1), 2)))
    k = pow(math.sin((lat2 - lat1) / 2), 2) + math.cos(lat1) * math.cos(lat2) * pow(math.sin((lng2 - lng1) / 2), 2)
    c = 2 * math.atan2(math.sqrt(k), math.sqrt(1 - k))
    dis = abs(R * c)
    return dis


n = 111000                 # 在地球赤道附近经度每差1度，实际距离相隔约111km
error = 100                # 100m
d = 20000
step = error / n / 3.3     # 0.0001


def baseIterativeAlgorithm(lng1, lat1, lng2, lat2, lng3, lat3, lng4, lat4, t1, t2, t3, t4):
    D21 = (t2 - t1) * c
    D31 = (t3 - t1) * c
    D41 = (t4 - t1) * c
    minLng = min([lng1, lng2, lng3, lng4]) - d / n
    minLat = min([lat1, lat2, lat3, lat4]) - d / n
    maxLng = max([lng1, lng2, lng3, lng4]) + d / n
    maxLat = max([lat1, lat2, lat3, lat4]) + d / n
    lng = minLng
    lat = minLat
    min_e = max(maxLng, maxLat)
    opt_lng = maxLng
    opt_lat = maxLat
    while lng <= maxLng:
        while lat <= maxLat:
            d01 = haversine(lng1, lat1, lng, lat)
            d02 = haversine(lng2, lat2, lng, lat)
            d03 = haversine(lng3, lat3, lng, lat)
            d04 = haversine(lng4, lat4, lng, lat)
            E21 = abs((d02 - d01) - D21)
            E31 = abs((d03 - d01) - D31)
            E41 = abs((d04 - d01) - D41)
            EF = E21 + E31 + E41
            if EF < min_e:
                min_e = EF
                opt_lng = lng
                opt_lat = lat
            lat += step
        lat = minLat
        lng += step
    return (opt_lng, opt_lat, min_e)