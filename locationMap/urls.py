from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from locationMap.views import *

urlpatterns = [
   url(r'^getGw$', getGw.as_view()),
   url(r'^getEd$', getEd.as_view()),
   url(r'^getAllData$', getAllData.as_view()),
]