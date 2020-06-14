from django.urls import path,include
from . import views
from rest_framework.urlpatterns import format_suffix_patterns
# from rest_framework import routers

# router = routers.DefaultRouter()
# router.register('my_book_detail/<str:device>',views.PlantaddViewSet)
urlpatterns = [
    # path('',include(router.urls)),
    path('test/',views.index,name="index"),
    path('result/<str:device>/<str:date>/',views.plant_result),
    path('plantcon/<str:name>/',views.plant_con),
    path('book_post/',views.book_post,name="book_post"),
    path('book_list/<str:device>/',views.book_list),
    path('my_book_detail/<str:device>/<str:id>/', views.my_book_detail),
    path('my_book_delete/<str:id>/', views.my_book_delete),
]
urlpatterns = format_suffix_patterns(urlpatterns)