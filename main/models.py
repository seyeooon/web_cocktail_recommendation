from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    base_liquor = models.JSONField(default=list, blank=True)
    alcohol_strength = models.JSONField(default=list, blank=True)
    glass = models.JSONField(default=list, blank=True)
    technique = models.JSONField(default=list, blank=True)

    def __str__(self):
        return self.user.username
