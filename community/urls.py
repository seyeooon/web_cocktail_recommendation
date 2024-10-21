from django.urls import path
from . import views

urlpatterns = [
    path('', views.general_community, name='general_community'),
    path('<str:cocktail_name>/', views.cocktail_community, name='cocktail_community'),
    path('add_comment/general/', views.add_comment, name='add_comment'),
    path('add_comment/<str:cocktail_name>/', views.add_comment, name='add_cocktail_comment'),
    
    # 댓글 삭제를 위한 경로 추가
    path('delete_comment/<int:comment_id>/', views.delete_comment, name='delete_general_comment'),
    path('delete_comment/<int:comment_id>/<str:cocktail_name>/', views.delete_comment, name='delete_comment'),
]