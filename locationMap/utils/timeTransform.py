import time
import datetime

def utc_to_timestamps(utctime):
    year = int(utctime[0:4])
    month = int(utctime[5:7])
    day = int(utctime[8:10])
    hour = int(utctime[11:13])
    minute = int(utctime[14:16])
    second = int(utctime[17:19])
    millsecond = int(utctime[20:26]) / 1e6
    t = datetime.datetime(year, month, day, hour, minute, second)
    tf = time.mktime(t.timetuple()) + millsecond
    return tf


#  "2018-07-25T13:54:09.483813Z" 1532498049483.813 "tmms":1216562068483
#  "2018-07-25T13:54:17.538693Z" 1532498057538.693 "tmms":1216562076538