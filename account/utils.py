from django.contrib.auth.models import User
from .models import Otp
from random import randint

def generate_otp(user):
    qs = Otp.objects.filter(user=user)
    qs.update(is_used=True)
    new_otp = randint(1000,9999)
    Otp.objects.create(user=user,otp=new_otp)
    return new_otp