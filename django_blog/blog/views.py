from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.forms import AuthenticationForm

# Registration view
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # log in user after registration
            messages.success(request, f'Account created for {user.username}!')
            return redirect('home')  # redirect to home or blog list page
    else:
        form = UserRegisterForm()
    return render(request, 'blog/register.html', {'form': form})

# Profile view
@login_required
def profile_view(request):
    return render(request, 'blog/profile.html')
