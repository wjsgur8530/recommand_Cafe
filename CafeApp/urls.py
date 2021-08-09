from django.urls import path
from CafeApp.views import *

urlpatterns = [
    path('', home, name='home'),
    path('map/', cafe_map, name='map'),
    path('search/', search_result, name='search'),
    path('crawling/', crawling, name='crawling'),
    path('detail/<int:pk>/', cafe_detail, name='detail'),
    path('theme/', category, name='theme'),
    path('theme/result/', category_result, name='category_result'),
]
