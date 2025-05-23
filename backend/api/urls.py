
from django.urls import path
from .views import SendOTPView, VerifyOTPView, RegisterUserView, RegisterLeadView

urlpatterns = [
    path('api/send-otp/', SendOTPView.as_view(), name='send-otp'),
    path('api/verify-otp/', VerifyOTPView.as_view(), name='verify-otp'),
    path('api/register-user/', RegisterUserView.as_view(), name='register-user'),
    path('api/register-lead/', RegisterLeadView.as_view(), name='register-lead'),
]
 