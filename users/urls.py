from django.urls import path
from .views import UserRegistrationView, user_login, UserProfileView

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', user_login, name='login'),
    path('profile/', UserProfileView.as_view(), name='profile'),
]