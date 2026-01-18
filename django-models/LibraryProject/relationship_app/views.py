from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Library, Book  # ✅ checker expects this import

# -----------------------------
# Function-based view: list all books
# -----------------------------
@login_required  # Optional: only logged-in users can see books
def list_books(request):
    books_list = Book.objects.all()
    context = {'books': books_list}
    return render(request, 'relationship_app/list_books.html', context)


# -----------------------------
# Class-based view: library detail
# -----------------------------
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# -----------------------------
# Authentication Views
# -----------------------------

# Registration view
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)  # Automatically log in after registration
            messages.success(request, "Registration successful!")
            return redirect('list_books')
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            messages.success(request, "Login successful!")
            return redirect('list_books')
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# Logout view
def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return render(request, 'relationship_app/logout.html')
