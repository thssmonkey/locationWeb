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
class Home(APIView):

    def get(self, request):
        return Response({'gid': 1, 'name': 'lora-gw', 'coordinate': '10.32,902.45'}, status=status.HTTP_200_OK)
