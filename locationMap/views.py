from django.shortcuts import render
import os
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password, check_password
from locationMap.models import *

# Create your views here.
# get gateway data
class getGw(APIView):
    def get(self, request):
        return Response([{'gid': 1, 'name': 'lora-gw1', 'coordinate': '115.12,39.65'},
                         {'gid': 2, 'name': 'lora-gw2', 'coordinate': '117.32,39.75'},
                         {'gid': 3, 'name': 'lora-gw3', 'coordinate': '117.42,39.21'},
                         {'gid': 4, 'name': 'lora-gw4', 'coordinate': '115.22,39.15'}],
                        status=status.HTTP_200_OK)

# get end-device data
class getEd(APIView):
    def get(self, request):
        return Response([{'eid': 1, 'name': 'end-device1', 'coordinate': '116.32,39.45'},
                         {'eid': 2, 'name': 'end-device2', 'coordinate': '116.31,39.35'}],
                        status=status.HTTP_200_OK)


# get gateway and end-device data
class getAllData(APIView):
    def get(self, request):
        return Response([{'gid': 1, 'name': 'lora-gw1', 'coordinate': '115.12,39.65'},
                         {'gid': 2, 'name': 'lora-gw2', 'coordinate': '117.32,39.75'},
                         {'gid': 3, 'name': 'lora-gw3', 'coordinate': '117.42,39.21'},
                         {'gid': 4, 'name': 'lora-gw4', 'coordinate': '115.22,39.15'},
                         {'eid': 1, 'name': 'end-device1', 'coordinate': '116.32,39.45'},
                         {'eid': 2, 'name': 'end-device2', 'coordinate': '116.31,39.35'}],
                        status=status.HTTP_200_OK)