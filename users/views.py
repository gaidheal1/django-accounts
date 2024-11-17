from datetime import timedelta
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.http import HttpResponse
from django.utils import timezone
from .models import Profile, Activity, Skill, UserAchievement, Achievement, GlobalStats
from .forms import ProfileForm, ActivityForm


def index(request):
    return render(request, 'index.html')

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
        else:
            messages.error(request, 'Invalid credentials')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


# Logout view
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def dashboard(request):
    activities = Activity.objects.filter(user=request.user) #.order_by('-created') # Optional ordering instead of in model
    skills = Skill.objects.filter(user=request.user)

    # Get the filter from the request (defaults to "daily")
    filter_by = request.GET.get('filter', 'daily')

    # Apply date filters based on the selected view (daily, weekly, monthly)
    if filter_by == 'daily':
        today = timezone.now().date()
        activities = activities.filter(created__date=today)
    elif filter_by == 'weekly':
        one_week_ago = timezone.now() - timedelta(days=7)
        activities = activities.filter(created__gte=one_week_ago)
    elif filter_by == 'monthly':
        one_month_ago = timezone.now() - timedelta(days=30)
        activities = activities.filter(created__gte=one_month_ago)

    # Pagination (10 activities per page)
    paginator = Paginator(activities, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Achievements
    unlocked = UserAchievement.objects.filter(user=request.user)

    stats = GlobalStats.objects.all()

    return render(request, 'dashboard.html', {
        'page_obj': page_obj,
        'filter_by': filter_by,
        'skills': skills,
        'unlocked': unlocked,
        'stats': stats,
        })

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    return render(request, 'profile.html', {'profile':profile})

@login_required
def edit_profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    return render(request, 'edit_profile.html', {'form': form})

@login_required
def add_activity(request):
    if request.method == 'POST':
        form = ActivityForm(request.POST, user=request.user)
        if form.is_valid():
            activity = form.save(commit=False)
            
            activity.user = request.user
            activity.save()
            
            profile = get_object_or_404(Profile, user=request.user)
            profile.add_xp(10*activity.time)

            messages.success(request, 'Your activity has been successfully added!')
            messages.success(request, f'You got {10*activity.time} XP')
            return redirect('dashboard')
        else:
            messages.error(request, 'There was an error adding your activity. Please try again.')
            print(form.errors)
    else:
        form = ActivityForm(user=request.user)
    return render(request, 'add_activity.html', {'form': form})

@login_required
def add_skill(request):
    if request.method == 'POST':
        skill_name = request.POST.get('skill_name')
        if skill_name:
            Skill.objects.create(name=skill_name, user=request.user)
        return redirect('add_activity')
    return HttpResponse("Invalid method", status=405)

@login_required
def leaderboard(request):
    profiles = Profile.objects.all().order_by('-level')
    return render(request, 'leaderboard.html', {
        'profiles': profiles,
        'current_user': request.user,
        })