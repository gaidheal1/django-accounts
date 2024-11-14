# users/urls.py
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views  # Import Django's auth views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),  # Use auth_views
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),  # Use auth_views
]
