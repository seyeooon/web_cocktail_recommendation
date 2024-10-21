from django.db import models

# Create your models here.

class Cocktail(models.Model):
    name = models.CharField(max_length=100)
    base_liquor = models.CharField(max_length=100)
    ingredients = models.JSONField()  # 재료를 JSON으로 저장
    garnish = models.CharField(max_length=100, blank=True)
    alcohol_strength = models.CharField(max_length=50)
    glass = models.CharField(max_length=100)
    color = models.CharField(max_length=50)
    technique = models.CharField(max_length=100)
    recipe = models.TextField(blank=True)  # 레시피
    tip = models.TextField(blank=True)  # 팁
    
    def __str__(self):
        return self.name  # 칵테일 이름을 객체의 문자열 표현으로 사용
