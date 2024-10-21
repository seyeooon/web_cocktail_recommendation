
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('main.urls')),  # main 앱의 URL 패턴 포함
    path('login/', include('login.urls')),  # login 앱의 URL 연결
    path('community/', include('community.urls')),  # community 앱의 URL 연결
    path('search/', include('search.urls')),  # search 앱 연결
    path('cocktail/', include('cocktail.urls')),  # cocktail 앱의 URL 패턴 포함
    
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),  # 로그아웃 처리
]

