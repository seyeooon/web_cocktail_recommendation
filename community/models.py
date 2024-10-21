# community/models.py
from django.db import models
from cocktail.models import Cocktail  # 칵테일 모델 불러오기
from django.contrib.auth.models import User
class Comment(models.Model):
    cocktail = models.CharField(max_length=100, null=True, blank=True)  # 칵테일 이름과 연결
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=100)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

