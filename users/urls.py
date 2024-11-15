# users/urls.py
from django.urls import path
from . import views
# from django.contrib.auth import views as auth_views  # Import Django's auth views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('login/', views.login_view, name='login'),  # Use auth_views
    path('logout/', views.logout_view, name='logout'),  # Use auth_views
    path('', views.index, name='index'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('add_activity/', views.add_activity, name='add_activity')
]
