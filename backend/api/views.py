import random
from django.core.mail import send_mail
from django.core.cache import cache
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import login
 

from .serializers import (
    SendOTPSerializer,
    VerifyOTPSerializer,
    RegisterUserSerializer,
    RegisterLeadSerializer,
)
from api.models import Lead
 
OTP_EXPIRY_SECONDS = 300
 
 
class SendOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SendOTPSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        email = serializer.validated_data['email']

        # ⛔ Check cooldown
        if cache.get(f"otp_cooldown:{email}"):
            return Response({'detail': 'Please wait before requesting another OTP.'}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        # ✅ Generate and save OTP
        otp = str(random.randint(100000, 999999))
        cache.set(f"otp:{email}", otp, timeout=OTP_EXPIRY_SECONDS)

        # ✅ Set cooldown
        cache.set(f"otp_cooldown:{email}", True, timeout=30)  # 60 seconds cooldown

        # ✅ Send OTP email
        try:
            send_mail(
                'Your OTP Code',
                f'Your OTP is {otp}. It expires in 5 minutes.',
                'trialofproject@gmail.com',
                [email],
                fail_silently=False,
            )
        except Exception as e:
            return Response({'detail': f'Failed to send OTP: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({'detail': 'OTP sent to your email'}, status=status.HTTP_200_OK)
 

 

 
class VerifyOTPView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        # Check if user is already authenticated
        if request.user.is_authenticated:
            return Response({'detail': 'You are already logged in.'}, status=status.HTTP_400_BAD_REQUEST)

        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'detail': 'Email and OTP required.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get the cached OTP for the email
        cached_otp = cache.get(f"otp:{email}")
        if cached_otp != otp:
            return Response({'detail': 'Invalid or expired OTP.'}, status=status.HTTP_400_BAD_REQUEST)

        # Get or create user
        user, _ = User.objects.get_or_create(username=email, email=email)

        # Log the user in (creates session cookie)
        login(request, user)

        # Delete OTP from cache after successful use
        cache.delete(f"otp:{email}")

        return Response({
            'detail': f'Logged in as {email}',
            'user': {
                'email': user.email,
                'username': user.username
            }
        }, status=status.HTTP_200_OK)


class RegisterUserView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated = serializer.validated_data
        user = User.objects.create_user(
          username=validated['email'], 
            email=validated['email'],
            first_name=validated['first_name'],
            last_name=validated['last_name']
        )
        user.save()

        return Response({'detail': 'User registered successfully'}, status=status.HTTP_201_CREATED)
 

class RegisterLeadView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterLeadSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        return Response({'message': 'Lead registered successfully'}, status=status.HTTP_201_CREATED)

 
