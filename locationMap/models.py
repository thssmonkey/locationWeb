from django.db import models
from django.utils import timezone

# Create your models here.

class EndDevice(models.Model):
    eid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    coordinate = models.CharField(max_length=60)

class GateWay(models.Model):
    gid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    coordinate = models.CharField(max_length=60)
    # jsondata = models.CharField(max_length=500)

class Data(models.Model):
    did = models.AutoField(primary_key=True)
    time = models.DateTimeField(default=timezone.now)
    jsondata = models.CharField(max_length=500)
    mtmfed = models.ManyToManyField(EndDevice)
    mtmfgw = models.ManyToManyField(GateWay)
