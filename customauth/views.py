from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import login, logout
from django.core.mail import send_mail
from django.http import JsonResponse
from django.middleware.csrf import get_token  # CSRF token handling
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from .models import CustomUser
from .serializers import UserSerializer, LoginSerializer
from datetime import datetime, timedelta

# Kullanıcı Kayıt
class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

# Kullanıcı Giriş
@method_decorator(ensure_csrf_cookie, name='dispatch')
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            login(request, user)
            print("Login Request Data:", request.data)
            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)
            response.set_cookie("csrftoken", get_token(request))  # CSRF token in cookies
            return response
        print("Login Error Data:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Kullanıcı Çıkış
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)

# CSRF Token Döndürme
def csrf_token_view(request):
    """API endpoint to fetch CSRF token"""
    return JsonResponse({'csrfToken': get_token(request)})

# Şifre Sıfırlama E-posta Gönderme
def password_reset_email(request):
    send_mail(
        'Password Reset',
        'Here is the link to reset your password.',
        'senseistrategyoffical@gmail.com',  # Gönderen e-posta adresi
        ['recipient@example.com'],  # Alıcı e-posta adresi
        fail_silently=False,
    )
    return JsonResponse({"message": "Password reset email sent successfully"})

# Abonelik Durumu Kontrol API'si
class SubscriptionStatusView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        subscription_end_date = user.subscription_end_date
        if subscription_end_date and subscription_end_date > datetime.now().date():
            remaining_days = (subscription_end_date - datetime.now().date()).days
            return Response({"status": "active", "remaining_days": remaining_days})
        else:
            return Response({"status": "inactive", "message": "No active subscription."})

# Kullanıcı Bilgileri (My Account) API'si
class MyAccountView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        user = request.user
        subscription_status = (
            "active"
            if user.subscription_end_date and user.subscription_end_date > datetime.now().date()
            else "inactive"
        )
        remaining_days = (
            (user.subscription_end_date - datetime.now().date()).days
            if user.subscription_end_date
            else 0
        )
        data = {
            "email": user.email,
            "subscription_status": subscription_status,
            "remaining_days": remaining_days,
        }
        return Response(data)

# Abonelik Satın Alma API'si
class SubscriptionPurchaseView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        subscription_type = request.data.get("subscription_type")

        if subscription_type == "30_days":
            user.subscription_end_date = datetime.now().date() + timedelta(days=30)
        elif subscription_type == "1_year":
            user.subscription_end_date = datetime.now().date() + timedelta(days=365)
        else:
            return Response(
                {"error": "Invalid subscription type"}, status=status.HTTP_400_BAD_REQUEST
            )

        user.is_subscription_active = True
        user.save()

        return Response(
            {"message": "Subscription purchased successfully"},
            status=status.HTTP_200_OK,
        )
