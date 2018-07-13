from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings
from locationMap.views import *

urlpatterns = [
   url(r'^home$', Home.as_view()),
]