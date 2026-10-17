from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register,name='register'),
    path('signin/',views.signin,name='signin'),
    path('home/',views.home,name='home'),
    path('signout/',views.signout,name='signout'),
    path('updatepassword/',views.updatepassword,name='updatepassword'),
    path('forgotpassword/',views.request_reset_password,name='forgotpassword'),
    path('resetpassword/<int:pk>/',views.reset_password,name='resetpassword'),
    path('validateotp/<int:pk>/', views.validate_otp, name='validateotp')
]