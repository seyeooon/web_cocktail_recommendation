# main/urls.py
from django.urls import path
from . import views  # main 앱의 views 모듈을 가져옴

urlpatterns = [
    path('', views.main_page, name='main_page'),  # 메인 페이지 URL 패턴
    path('recommend_cocktails/', views.recommend_cocktails, name='recommend_cocktails'),  # 추천 칵테일 경로
    path('recommend_personalized_cocktails/', views.recommend_personalized_cocktails, name='recommend_personalized_cocktails'),
    path('my_page/', views.my_page, name='my_page'),  # 마이페이지 경로 추가
    path('my_page/save_preferences/', views.save_preferences, name='save_preferences'),
]