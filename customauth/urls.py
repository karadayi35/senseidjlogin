from django.urls import path
from .views import csrf_token_view
from .views import (
    RegisterView,
    LoginView,
    LogoutView,
    password_reset_email,
    csrf_token_view,  # Doğru fonksiyon ismi
    SubscriptionStatusView,
    MyAccountView,
    SubscriptionPurchaseView,
)

urlpatterns = [
    path("send-email/", password_reset_email, name="send_email"),
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path('csrf/', csrf_token_view, name='csrf_token'),
    path("subscription-status/", SubscriptionStatusView.as_view(), name="subscription_status"),
    path("my-account/", MyAccountView.as_view(), name="my_account"),
    path("purchase-subscription/", SubscriptionPurchaseView.as_view(), name="purchase_subscription"),
]
