from django.shortcuts import render,redirect
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm,PasswordChangeForm,SetPasswordForm
from django.http import HttpResponse
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from .forms import UserForm,IdentifyUser,RegisterForm
from django.core.mail import send_mail
from django.contrib import messages
from django.contrib.auth.models import User
from .utils import generate_otp
from .forms import OtpVerifyForm
# Create your views here.


def signin(request):
    if request.method == 'POST':
        fm = AuthenticationForm(request,request.POST)
        if fm.is_valid():
            user = fm.get_user()
            login(request,user)
            return redirect('home')
        context = {'form':fm}
        return render(request,'signin.html',context)
    context = {'form':AuthenticationForm()}
    return render(request,'signin.html',context)

def register(request):
    if request.method == 'POST':
        fm = RegisterForm(request.POST)
        if fm.is_valid():
            fm.save()
            email = fm.cleaned_data.get('email')
            firstname = fm.cleaned_data.get('firs_tname')
            lastname = fm.cleaned_data.get('last_name')
            send_mail(
                'User Success',
                f'Welcome to django {firstname} {lastname}',
                'codegod1609@gmail.com',
                [email],
                fail_silently= True
            )
            messages.success(request,f'User {firstname} {lastname} registered successfully')
            return redirect('signin')
        context = {'form':fm}
        return render(request,"register.html",context)
    context = {'form':RegisterForm()}
    return render(request,"register.html",context)

@login_required(login_url='signin')
def home(request):
    return render(request,'home.html')

def signout(request):
    if request.method == 'POST':
        logout(request)
        return redirect('signin')
    return render(request,'signout.html')

@login_required
def updatepassword(request):
    user = request.user
    if request.method == 'POST':
        fm = PasswordChangeForm(user=user,data=request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('signin')
        context = {'form':fm}
        return render(request,'updatepassword.html',context)
    context = {'form':PasswordChangeForm(user=user)}
    return render(request,'updatepassword.html',context)

# def request_reset_password(request):
#     if request.method == 'POST':
#         fm = IdentifyUser(request.POST)
#         if fm.is_valid():
#             username = fm.cleaned_data.get('username')
#             user = User.objects.get(username=username)
#             url = f'http://127.0.0.1:8000/account/{user.pk}/'
#             send_mail(
#                 'reset_password',
#                 f'here is your reset password link {url}',
#                 'codegod1630@gmail.com',
#                 [user.email],
#                 fail_silently=True
#             )
#             messages.success(request,f'reset password link to your {user.email}')
#             return redirect('signin')
#         context = {'form':fm}
#         return render(request,'forgotpassword.html',context)
#     context = {'form':IdentifyUser()}
#     return render(request,'forgotpassword.html',context)

def reset_password(request,pk):
    user = User.objects.get(pk=pk)
    if request.method == 'POST':
        fm = SetPasswordForm(user=user,data=request.POST)
        if fm.is_valid():
            fm.save()
            return redirect('signin')
        context = {'form':fm}
        return render(request,'reset_password.html',context)
    context = {'form': SetPasswordForm(user=user)}
    return render(request,'reset_password.html',context)

def request_reset_password(request):
    if request.method == 'POST':
        fm = IdentifyUser(request.POST)
        if fm.is_valid():
            username = fm.cleaned_data.get('username')
            user = User.objects.get(username=username)
            otp = generate_otp(user)
            send_mail(
                'reset_password',
                f'here is your otp {otp}',
                'codegod1609@gmail.com',
                [user.email],
                fail_silently=False
            )
            messages.success(request,f'reset password link sended to your {user.email}')
            return redirect('validateotp',pk=user.pk)
        context = {'form':fm}
        return render(request,'forgotpassword.html',context)
    context = {'form':IdentifyUser()}
    return render(request,'forgotpassword.html',context)

def validate_otp(request,pk):
    if request.method == 'POST':
        fm = OtpVerifyForm(user_id = pk,data=request.POST)
        if fm.is_valid():
            messages.success(request,'otp Validated successfully')
            return redirect(f'/account/resetpassword/{pk}/')
        context = {'form':fm}
        return render(request,'validate_otp.html',context)
    context = {'form':OtpVerifyForm(user_id=pk)}
    return render(request,'validate_otp.html',context)