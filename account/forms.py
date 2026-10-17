from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Otp
from django.utils import timezone
from datetime import timedelta

class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','email','username','password1','password2']

class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','password1','password2']
        widgets = {
            'username' : forms.TextInput(
                attrs={
                    'class':'form-control',
                    'placeholder':'Enter username'
                }
            )
        }




class IdentifyUser(forms.Form):
    username = forms.CharField(max_length=100)

    def clean_username(self):
        username = self.cleaned_data['username']

        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(
                'User not found with this username'
            )

        return username


class OtpVerifyForm(forms.Form):
    otp = forms.IntegerField()

    def __init__(self,*args,**kwargs):
        self.user_id = kwargs.pop('user_id')
        super().__init__(*args,**kwargs)

    def clean_otp(self):
        otp = self.cleaned_data.get('otp')
        user = User.objects.get(id = self.user_id)

        qs = Otp.objects.filter(user=user,otp=otp)
        if not qs.exists():
            raise forms.ValidationError('invalid otp')
        otp_obj = qs[0]
        if otp_obj.is_used:
            raise forms.ValidationError('otp Already used')
        if timezone.now() - otp_obj.created_at > timedelta(minutes=2):
            otp_obj.is_expired = True
            otp_obj.save()
            raise forms.ValidationError('your time limit is expired')
        if otp_obj.is_expired:
            raise forms.ValidationError('otp is exp')
        otp_obj.is_used = True
        otp_obj.save()
        return otp

    