from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import RegisterForm, LoginForm, ProfileForm
from .models import Player


def register_view(request):
    if request.user.is_authenticated:
        return redirect('challenges:list')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            player = form.save()
            login(request, player)
            messages.success(request, f'Welcome to the arena, {player.username}!')
            return redirect('challenges:list')
    else:
        form = RegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('challenges:list')
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            return redirect(request.GET.get('next', 'challenges:list'))
    else:
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def profile_view(request, username=None):
    if username:
        player = get_object_or_404(Player, username=username)
    else:
        player = request.user

    solves = player.submissions.filter(is_correct=True).select_related('challenge').order_by('-submitted_at')
    return render(request, 'accounts/profile.html', {
        'player': player,
        'solves': solves,
        'is_own': player == request.user,
    })


@login_required
def edit_profile_view(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated!')
            return redirect('accounts:profile')
    else:
        form = ProfileForm(instance=request.user)
    return render(request, 'accounts/edit_profile.html', {'form': form})
