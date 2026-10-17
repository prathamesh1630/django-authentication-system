from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Otp(models.Model):
    otp = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_used = models.BooleanField(default=False)
    is_expired = models.BooleanField(default=False)
