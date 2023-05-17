from django.urls import path, include
from .views import *
app_name = 'core'
from rest_framework import routers
router = routers.DefaultRouter()
router.register('lane', StatusView, 'lane')

urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/lane/', StatusView.as_view(), name="lane"),
]