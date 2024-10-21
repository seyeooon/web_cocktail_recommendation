
from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='login_page'),
    path('signup/', views.signup_page, name='signup_page'),  # 회원가입 페이지 경로 추가
]
