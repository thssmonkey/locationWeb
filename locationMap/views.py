
import os
import json
from locationMap.models import *
from rest_framework import mixins
from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
# from utils.timeTransform import utc_to_timestamps
# from utils.location import threeAnchorCalculate
# from utils.coordTransform import wgs84_to_bd09, wgs84_to_cartesian, cartesian_to_wgs84

## gateway location(km)
'''
gateway_json = [{'gid': 1, 'name': 'lora-gw1', 'coordinate': '102.6570,24.9889'},
                {'gid': 2, 'name': 'lora-gw2', 'coordinate': '102.706879,25.049358'},
                {'gid': 3, 'name': 'lora-gw3', 'coordinate': '102.74032,25.012774'}]
enddevice_json = [{'eid': 1, 'name': 'end-device1', 'coordinate': '102.67065001365012,25.00255001365013'},
                {'eid': 2, 'name': 'end-device2', 'coordinate': '102.714763,25.029774'}]
                
gateway_json = [{'gid': 1, 'name': 'lora-gw1', 'coordinate': '102.6570,24.9889'},
                {'gid': 2, 'name': 'lora-gw2', 'coordinate': '102.706879,25.049358'},
                {'gid': 3, 'name': 'lora-gw3', 'coordinate': '102.74032,25.012774'}]
enddevice_json = [{'eid': 1, 'name': 'end-device1', 'coordinate': '116.32308,40.00822'},
                {'eid': 2, 'name': 'end-device2', 'coordinate': '116.32309,40.00822'}]


## device location(km)
realX = 102.714763
realY = 24.979197


rxInfo = [{'gatewayID': 'b827ebfffeee91c0', 'name': 'lorawan-gw', 'time': '2018-07-25T13:58:23.856203Z', 'rssi': -37, 'loRaSNR': 7.2, 'location': {'latitude': 24.9889, 'longitude': 102.6570, 'altitude': 44}}, {'gatewayID': 'b827ebfffeee91c1', 'name': 'lorawan-gw', 'time': '2018-07-25T13:58:45.335915Z', 'rssi': -39, 'loRaSNR': 5.8, 'location': {'latitude': 25.049358, 'longitude': 102.706879, 'altitude': 44}}, {'gatewayID': 'b827ebfffeee91c2', 'name': 'lorawan-gw', 'time': '2018-07-25T13:58:55.817835Z', 'rssi': -47, 'loRaSNR': 7.5, 'location': {'latitude': 25.012774, 'longitude': 102.74032, 'altitude': 44}}]

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
    TDOA21 = 0.000006
    TDOA31 = 0.000005
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
'''
gateway_json = [{'gid': 1, 'name': 'lora-gw1', 'coordinate': '102.6570,24.9889'},
                {'gid': 2, 'name': 'lora-gw2', 'coordinate': '102.706879,25.049358'},
                {'gid': 3, 'name': 'lora-gw3', 'coordinate': '102.74032,25.012774'}]
enddevice_json = [{'eid': 1, 'name': 'end-device1', 'coordinate': '102.67065001365012,25.00255001365013'},
                {'eid': 2, 'name': 'end-device2', 'coordinate': '102.714763,25.029774'}]

# Create your views here.
# get gateway data
class getGw(APIView):
    def get(self, request):
        gateway_set = GateWay.objects.all()
        return Response(gateway_json, status=status.HTTP_200_OK)

# get end-device data
class getEd(APIView):
    def get(self, request):
        enddevice_set = EndDevice.objects.all()
        return Response(enddevice_json, status=status.HTTP_200_OK)

# get gateway and end-device data
class getAllData(APIView):
    def get(self, request):
        gateway_set = GateWay.objects.all()
        enddevice_set = EndDevice.objects.all()
        return Response(gateway_json + enddevice_json, status=status.HTTP_200_OK)