# cocktail/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('<str:cocktail_name>/', views.cocktail_detail, name='cocktail_detail'),
]
