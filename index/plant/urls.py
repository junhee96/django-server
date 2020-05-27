from django.urls import path,include
from . import views
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('plant',views.PlantimageViewSet)
# router.register('account',views.TestViewSet)
urlpatterns = [
    # path('',include(router.urls)),
    # path('',views.main,name="main"),
    path('',views.index,name="index"),
]