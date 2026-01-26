from django.contrib.auth.decorators import permission_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView

from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import (
    login_required,
    permission_required,
    user_passes_test,
)
from django.contrib import messages
from django.http import HttpResponse
from .models import Library, Book


# =============================
# Books Views
# =============================
@login_required
def book_list(request):
    books_list = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books_list})
@login_required
def list_books(request):
    books_list = Book.objects.all()
    return render(request, 'relationship_app/list_books.html', {'books': books_list})

# @permission_required('relationship_app.can_edit', raise_exception=True) 
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'


# =============================
# Authentication Views
# =============================

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            messages.success(request, "Registration successful!")
            return redirect('list_books')
    else:
        form = UserCreationForm()

    return render(request, 'relationship_app/register.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            messages.success(request, "Login successful!")
            return redirect('list_books')
    else:
        form = AuthenticationForm()

    return render(request, 'relationship_app/login.html', {'form': form})


def logout_view(request):
    auth_logout(request)
    messages.info(request, "You have been logged out.")
    return render(request, 'relationship_app/logout.html')


# =============================
# Role-Based Access Control
# =============================

def is_admin(user):
    return user.userprofile.role == 'Admin'


def is_librarian(user):
    return user.userprofile.role == 'Librarian'


def is_member(user):
    return user.userprofile.role == 'Member'


@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')


@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')


@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# =============================
# Permission-Based Book Actions
# =============================

@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        author_id = request.POST.get('author')

        Book.objects.create(title=title, author_id=author_id)
        return redirect('list_books')

    return render(request, 'relationship_app/add_book.html')


@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.save()
        return redirect('list_books')

    return render(request, 'relationship_app/edit_book.html', {'book': book})


@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)

    if request.method == 'POST':
        book.delete()
        return redirect('list_books')

    return render(request, 'relationship_app/delete_book.html', {'book': book})
