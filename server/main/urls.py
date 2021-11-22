from django.conf.urls import url, include
from rest_framework import routers

from . import views

router = routers.DefaultRouter()
router.register('DataLake', views.DataLakeViewSet)

urlpatterns = [
    url(r'', include(router.urls)),
]
