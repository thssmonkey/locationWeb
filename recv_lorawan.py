#!/usr/bin/env python3
import os
import django
# 外来脚本加如下两句才可引用项目模块
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "locationWeb.settings")
django.setup()

import sys
import json
from locationMap.archive.Logger import Logger
from flask import Flask, request
from locationMap.models import *
from django.db.models import Q
from locationMap.utils.timeTransform import utc_to_timestamps
from locationMap.utils.location import threeAnchorCalculate
from locationMap.utils.coordTransform import wgs84_to_bd09, wgs84_to_cartesian, cartesian_to_wgs84

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
GLOBAL = json.loads(open(os.path.join(BASE_DIR, 'global.json')).read())

logs_path = 'archive/logs/'
if not os.path.exists(logs_path):
    os.makedirs(logs_path)

device_logger = {}

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def loranode():
    try:
        mjson = request.get_json()
        if request.method == 'POST':
            rxInfo = mjson['rxInfo']
            if len(rxInfo) == GLOBAL['GATEWAY_NUM']:
                (gateway_json, enddevice_json) = getDeviceLocation(rxInfo)
                # 将网关插入数据库中
                for gw in gateway_json:
                    res = GateWay.objects.filter(gid=gw['gid'])
                    if not res:
                        instance = GateWay(gid=gw['gid'], name=gw['name'], coordinate=gw['coordinate'])
                        instance.save()
                    else:
                        GateWay.objects.get(gid=['gid']).update(name=gw['name'], coordinate=gw['coordinate'])
                GateWay.objects.filter(~Q(gid=gateway_json[0]['gid']) & ~Q(gid=gateway_json[1]['gid']) & ~Q(gid=gateway_json[2]['gid'])).delete()
                # 将终端节点插入数据库中
                for ed in enddevice_json:
                    res = EndDevice.objects.filter(eid=ed['eid'])
                    if not res:
                        instance = EndDevice(eid=ed['eid'], name=ed['name'], coordinate=ed['coordinate'])
                        instance.save()
                    else:
                        EndDevice.objects.get(eid=['eid']).update(name=ed['name'], coordinate=ed['coordinate'])
            # 记录在log日志中
            # devide_path = mjson['devEUI'] + '.log'
            devide_path = mjson['deviceName'] + '.log'
            device_logger = Logger(devide_path, logfile=logs_path + devide_path).get_logger()
            device_logger.info(mjson)
            return 'OK'
        else:
            return mjson
    except Exception:
        return 'OK'

def getDeviceLocation(rxInfo):
    gateway_json = []
    enddevice_json = []
    for info in rxInfo:
        gw_id = info['gatewayID']
        gw_name = info['name']
        gw_time = info['time']
        gw_coor = str(info['location']['longitude']) +  ',' + str(info['location']['latitude'])
        gateway_json.append({'gid': gw_id, 'name': gw_name, 'time': gw_time, 'coordinate': gw_coor})
    (x1, y1) = wgs84_to_cartesian(float(gateway_json[0]['coordinate'].split(",")[0]), float(gateway_json[0]['coordinate'].split(",")[1]))
    (x2, y2) = wgs84_to_cartesian(float(gateway_json[1]['coordinate'].split(",")[0]), float(gateway_json[1]['coordinate'].split(",")[1]))
    (x3, y3) = wgs84_to_cartesian(float(gateway_json[2]['coordinate'].split(",")[0]), float(gateway_json[2]['coordinate'].split(",")[1]))
    TDOA21 = utc_to_timestamps(gateway_json[1]['time']) - utc_to_timestamps(gateway_json[0]['time'])
    TDOA31 = utc_to_timestamps(gateway_json[2]['time']) - utc_to_timestamps(gateway_json[0]['time'])
    ((r1, X1, Y1), (r2, X2, Y2)) = threeAnchorCalculate(x1, y1, x2, y2, x3, y3, TDOA21, TDOA31)
    edX = 0
    edY = 0
    if r1 > 0:
        (edX, edY) = (X1, Y1)
    if r2 > 0:
        (edX, edY) = (X2, Y2)
    ed_id = '212'
    ed_name = 'end-device'
    (edlng, edlat) = cartesian_to_wgs84(edX, edY)
    ed_coor = str(edlng) + ',' + str(edlat)
    enddevice_json.append({'eid': ed_id, 'name': ed_name, 'coordinate': ed_coor})
    #  将gps坐标转为百度系坐标
    for gw in gateway_json:
        lng, lat = wgs84_to_bd09(float(gw['coordinate'].split(",")[0]), float(gw['coordinate'].split(",")[1]))
        gw['coordinate'] = str(lng) + ',' + str(lat)
    for ed in enddevice_json:
        lng, lat = wgs84_to_bd09(float(ed['coordinate'].split(",")[0]), float(ed['coordinate'].split(",")[1]))
        ed['coordinate'] = str(lng) + ',' + str(lat)
    return (gateway_json, enddevice_json)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7777)

