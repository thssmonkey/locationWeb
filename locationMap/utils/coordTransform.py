# -*- coding: utf-8 -*-import sys, getopt
import json
import urllib
import math

x_pi = 3.14159265358979324 * 3000.0 / 180.0
pi = 3.1415926535897932384626  # π
a = 6378245.0  # 长半轴
ee = 0.00669342162296594323  # 偏心率平方


class Geocoding:
    def __init__(self, api_key):
        self.api_key = api_key

    def geocode(self, address):
        """
        利用高德geocoding服务解析地址获取位置坐标
        :param address:需要解析的地址
        :return:
        """
        geocoding = {'s': 'rsv3',
                     'key': self.api_key,
                     'city': '全国',
                     'address': address}
        geocoding = urllib.urlencode(geocoding)
        ret = urllib.urlopen("%s?%s" % ("http://restapi.amap.com/v3/geocode/geo", geocoding))

        if ret.getcode() == 200:
            res = ret.read()
            json_obj = json.loads(res)
            if json_obj['status'] == '1' and int(json_obj['count']) >= 1:
                geocodes = json_obj['geocodes'][0]
                lng = float(geocodes.get('location').split(',')[0])
                lat = float(geocodes.get('location').split(',')[1])
                return [lng, lat]
            else:
                return None
        else:
            return None


def gcj02_to_bd09(lng, lat):
    """
    火星坐标系(GCJ-02)转百度坐标系(BD-09)
    谷歌、高德——>百度
    :param lng:火星坐标经度
    :param lat:火星坐标纬度
    :return:
    """
    z = math.sqrt(lng * lng + lat * lat) + 0.00002 * math.sin(lat * x_pi)
    theta = math.atan2(lat, lng) + 0.000003 * math.cos(lng * x_pi)
    bd_lng = z * math.cos(theta) + 0.0065
    bd_lat = z * math.sin(theta) + 0.006
    return [bd_lng, bd_lat]


def bd09_to_gcj02(bd_lon, bd_lat):
    """
    百度坐标系(BD-09)转火星坐标系(GCJ-02)
    百度——>谷歌、高德
    :param bd_lat:百度坐标纬度
    :param bd_lon:百度坐标经度
    :return:转换后的坐标列表形式
    """
    x = bd_lon - 0.0065
    y = bd_lat - 0.006
    z = math.sqrt(x * x + y * y) - 0.00002 * math.sin(y * x_pi)
    theta = math.atan2(y, x) - 0.000003 * math.cos(x * x_pi)
    gg_lng = z * math.cos(theta)
    gg_lat = z * math.sin(theta)
    return [gg_lng, gg_lat]


def wgs84_to_gcj02(lng, lat):
    """
    WGS84转GCJ02(火星坐标系)
    :param lng:WGS84坐标系的经度
    :param lat:WGS84坐标系的纬度
    :return:
    """
    if out_of_china(lng, lat):  # 判断是否在国内
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [mglng, mglat]


def gcj02_to_wgs84(lng, lat):
    """
    GCJ02(火星坐标系)转GPS84
    :param lng:火星坐标系的经度
    :param lat:火星坐标系纬度
    :return:
    """
    if out_of_china(lng, lat):
        return [lng, lat]
    dlat = _transformlat(lng - 105.0, lat - 35.0)
    dlng = _transformlng(lng - 105.0, lat - 35.0)
    radlat = lat / 180.0 * pi
    magic = math.sin(radlat)
    magic = 1 - ee * magic * magic
    sqrtmagic = math.sqrt(magic)
    dlat = (dlat * 180.0) / ((a * (1 - ee)) / (magic * sqrtmagic) * pi)
    dlng = (dlng * 180.0) / (a / sqrtmagic * math.cos(radlat) * pi)
    mglat = lat + dlat
    mglng = lng + dlng
    return [lng * 2 - mglng, lat * 2 - mglat]


def bd09_to_wgs84(bd_lon, bd_lat):
    lon, lat = bd09_to_gcj02(bd_lon, bd_lat)
    return gcj02_to_wgs84(lon, lat)


def wgs84_to_bd09(lon, lat):
    lon, lat = wgs84_to_gcj02(lon, lat)
    return gcj02_to_bd09(lon, lat)


def _transformlat(lng, lat):
    ret = -100.0 + 2.0 * lng + 3.0 * lat + 0.2 * lat * lat + \
          0.1 * lng * lat + 0.2 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lat * pi) + 40.0 *
            math.sin(lat / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(lat / 12.0 * pi) + 320 *
            math.sin(lat * pi / 30.0)) * 2.0 / 3.0
    return ret


def _transformlng(lng, lat):
    ret = 300.0 + lng + 2.0 * lat + 0.1 * lng * lng + \
          0.1 * lng * lat + 0.1 * math.sqrt(math.fabs(lng))
    ret += (20.0 * math.sin(6.0 * lng * pi) + 20.0 *
            math.sin(2.0 * lng * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(lng * pi) + 40.0 *
            math.sin(lng / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(lng / 12.0 * pi) + 300.0 *
            math.sin(lng / 30.0 * pi)) * 2.0 / 3.0
    return ret


def out_of_china(lng, lat):
    """
    判断是否在国内，不在国内不做偏移
    :param lng:
    :param lat:
    :return:
    """
    return not (lng > 73.66 and lng < 135.05 and lat > 3.86 and lat < 53.55)


def wgs84_to_cartesian(lng, lat):
    city = "beijing"
    Datum = 84
    PI = math.pi
    iPI = math.pi / 180  # PI/180
    if Datum == 84:
        a = 6378137
        f = 1 / 298.257223563
    elif Datum == 54:
        a = 6378245
        f = 1 / 298.3
    elif Datum == 80:
        a = 6378140
        f = 1 / 298.257
    else:
		# 其他参数按照WGS84基准面为84处理
        a = 6378137
        f = 1 / 298.257223563
    b = (1 - f) * a
    e = math.sqrt(2 * f - f * f)
    e1 = e / math.sqrt(1 - e * e)

    L0 = 0                        # 暂时处理
    W0 = 0
    k0 = 1
    FE = 0
    FN = 0
    if city == "beijing":
        L0 = 116
    elif city == "shanghai":
        L0 = 121.5
    elif city == "chongqing":
        L0 = 107.5
    else:
        L0 = 116

    # 必要变量准备   
    B = (lat - W0) * iPI # 纬差弧度
    L = (lng - L0) * iPI # 经差弧度
    sinB = math.sin(B)
    cosB = math.cos(B)
    tanB = math.tan(B)
    N = a / math.sqrt(1 - pow(e * sinB, 2)) # 卯酉圈曲率半径
    g = e1 * cosB
 
	# 求解参数
    C = pow(a, 2) / b
    B0 = 1 - 3.0 / 4.0 * pow(e1, 2) + 45.0 / 64.0 * pow(e1, 4) - 175.0 / 256.0 * pow(e1, 6) + 11025.0 / 16384.0 * pow(e1, 8)
    B2 = B0 - 1
    B4 = 15.0 / 32.0 * pow(e1, 4) - 175.0 / 384.0 * pow(e1, 6) + 3675.0 / 8192.0 * pow(e1, 8)
    B6 = 0 - 35.0 / 96.0 * pow(e1, 6) + 735.0 / 2048.0 * pow(e1, 8)
    B8 = 315.0 / 1024.0 * pow(e1, 8)
    s = C * (B0 * B + sinB * (B2 * cosB + B4 * pow(cosB, 3) + B6 * pow(cosB, 5) + B8 * pow(cosB, 7)))
	# 求解平面直角坐标系坐标
    xTemp = s + pow(L, 2) * N * sinB * cosB / 2.0 + pow(L, 4) * N * sinB * pow(cosB, 3) * (5 - pow(tanB, 2) + 9 * pow(g, 2) + 4 * pow(g, 4)) / 24.0 + pow(L, 6) * N * sinB * pow(cosB, 5) * (61 - 58 * pow(tanB, 2) + pow(tanB, 4)) / 720.0
    yTemp = L * N * cosB + pow(L, 3) * N * pow(cosB, 3) * (1 - pow(tanB, 2) + pow(g, 2)) / 6.0 + pow(L, 5) * N * pow(cosB, 5) * (5 - 18 * pow(tanB, 2) + pow(tanB, 4) + 14 * pow(g, 2) 
    - 58 * pow(g, 2) * pow(tanB, 2)) / 120.0

    x = xTemp + FN
    y = yTemp + FE
 
    return (x, y)

def cartesian_to_wgs84(x, y):
    city = "beijing"
    Datum = 84
    PI = math.pi
    iPI = math.pi / 180  # PI/180
    if Datum == 84:
        a = 6378137
        f = 1 / 298.257223563
    elif Datum == 54:
        a = 6378245
        f = 1 / 298.3
    elif Datum == 80:
        a = 6378140
        f = 1 / 298.257
    else:
		# 其他参数按照WGS84基准面为84处理
        a = 6378137
        f = 1 / 298.257223563
    b = (1 - f) * a
    e = math.sqrt(2 * f - f * f)
    e1 = e / math.sqrt(1 - e * e)

    L0 = 0                        # 暂时处理
    W0 = 0
    k0 = 1
    FE = 0
    FN = 0
    if city == "beijing":
        L0 = 116
    elif city == "shanghai":
        L0 = 121.5
    elif city == "chongqing":
        L0 = 107.5
    else:
        L0 = 116

    El1 = (1 - math.sqrt(1 - pow(e, 2))) / (1 + math.sqrt(1 - pow(e, 2)))
    Mf = (x - FN) / k0 # 真实坐标值
    Q = Mf / (a * (1 - pow(e, 2) / 4.0 - 3 * pow(e, 4) / 64.0 - 5 * pow(e, 6) / 256.0))
    Bf = Q + (3 * El1 / 2.0 - 27 * pow(El1, 3) / 32.0) * math.sin(2 * Q) + (21 * pow(El1, 2) / 16.0 - 55 * pow(El1, 4) / 32.0) * math.sin(4 * Q) 
    + (151 * pow(El1, 3) / 96.0) * math.sin(6 * Q) + 1097 / 512.0 * pow(El1, 4) * math.sin(8 * Q)
    sinBf = math.sin(Bf)
    tanBf = math.tan(Bf)
    cosBf = math.cos(Bf)
    Rf = a * (1 - pow(e, 2)) / math.sqrt(math.pow(1 - pow(e * sinBf, 2), 3))
    Nf = a / math.sqrt(1 - pow(e * sinBf, 2)) # 卯酉圈曲率半径
    Tf = pow(tanBf, 2)
    D = (y - FE) / (k0 * Nf)
    Cf = pow(e1, 2) * pow(cosBf, 2)

    B = Bf - Nf * tanBf / Rf * (pow(D, 2) / 2.0 - (5 + 3 * Tf + 10 * Cf - 9 * Tf * Cf - 4 * pow(Cf, 2) - 9 * pow(e1, 2)) * pow(D, 4) / 24.0 
    + (61 + 90 * Tf + 45 * pow(Tf, 2) - 256 * pow(e1, 2) - 3 * pow(Cf, 2)) * pow(D, 6) / 720.0)
    L = L0 * iPI + 1 / cosBf * (D - (1 + 2 * Tf + Cf) * pow(D, 3) / 6.0 + (5 - 2 * Cf + 28 * Tf - 3 * pow(Cf, 2) + 8 * pow(e1, 2) + 24 * pow(Tf, 2)) * pow(D, 5) / 120.0)

    Bangle = B / iPI
    Langle = L / iPI

    latitude = Bangle + W0 # 纬度 B W x
    longitude = Langle # 经度 L J y
 
    return (longitude, latitude)

# print(wgs84_to_cartesian(120, 41))
# print(cartesian_to_wgs84(4548288, 336579))


'''  Warning： 经纬度没有转为弧度
def wgs84_to_cartesian(lng, lat, alt)：
    a = 6378137                # m
    b = 6.356752314245179e+06  # m
    p = math.pi / 180          # Pi/180
    lng = lng * p
    lat = lat * p
    e = (pow(a, 2) - pow(b, 2)) / pow(a, 2)
    v = a / (math.sqrt(1 - e * pow(math.sin(lng), 2)))
    X = (v +  alt) * math.cos(lat) * math.cos(lng)
    Y = (v + alt) * math.cos(lat) * math.sin(lng)
    Z = (v * (1 - e) + alt) * math.sin(lat)
    return (X, Y, Z)

# z = (z1 + z2 + z3 + z4) / 4
def cartesian_to_wgs84(x, y, z):
    a = 6378137                # m
    b = 6.356752314245179e+06  # m
    p = 180 / math.pi          # Pi/180
    e = (pow(a, 2) - pow(b, 2)) / pow(a, 2)
    el = e / (1 - e)
    theta = math.atan((z * a) / (p * b))
    p = math.sqrt(pow(x, 2) + pow(y, 2))
    lng = math.atan(y / x)
    lat = math.atan((z + el * b * pow(math.sin(theta), 3)) / (p - e * a * pow(math.cos(theta), 3)))
    return (lng * p, lat * p)

def wgs84_to_cartesian(lng, lat):
    baselng = 116.3972282409668
    baselat = 39.90960456049752
    MACRO_AXIS = 6378.137
    MINOR_AXIS = 6356.752
    # gey Y
    x0 = pow(MACRO_AXIS, 2.0) / math.sqrt(pow(MACRO_AXIS, 2.0) + pow(MINOR_AXIS, 2.0) * pow(math.tan(baselat), 2.0))
    y0 = pow(MINOR_AXIS, 2.0) / math.sqrt(pow(MINOR_AXIS, 2.0) + pow(MACRO_AXIS, 2.0) * pow(1 / math.tan(baselat), 2.0))
    x1 = pow(MACRO_AXIS, 2.0) / math.sqrt(pow(MACRO_AXIS, 2.0) + pow(MINOR_AXIS, 2.0) * pow(math.tan(lat), 2.0))
    y1 = pow(MINOR_AXIS, 2.0) / math.sqrt(pow(MINOR_AXIS, 2.0) + pow(MACRO_AXIS, 2.0) * pow(1 / math.tan(lat), 2.0))
    Y = math.sqrt(pow(x1 - x0, 2.0) + pow(y1 - y0, 2.0))
    # get X
    X = x0 * (lng - baselng)
    return (X, Y)
'''