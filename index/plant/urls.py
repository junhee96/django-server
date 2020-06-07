from django.urls import path,include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('plant',views.VersionViewSet)
# router.register('account',views.TestViewSet)
urlpatterns = [
    path('',include(router.urls)),
    path('main/',views.main,name="main"),
    path('test/',views.index,name="index"),
    path('result/<str:device>/<str:date>/',views.plant_result),
    path('plantcon/<str:name>/',views.plant_con),
]