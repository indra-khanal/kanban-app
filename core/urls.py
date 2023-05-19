from django.urls import path, include
from .views import BoardView, TagView, LaneView,CardView
app_name = 'core'
from rest_framework import routers
router = routers.DefaultRouter()
router.register('board', BoardView, 'board')
router.register('tags', TagView, 'tags')
router.register('lane', LaneView, 'lane')
router.register('card', CardView, 'card')




urlpatterns = [
    path('api/', include(router.urls)),
    # path('api/lane/', StatusView.as_view(), name="lane"),
]