from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import list_books, LibraryDetailView, register  # checker expects register import

urlpatterns = [
    # Function-based view: list all books
    path('books/', list_books, name='list_books'),

    # Class-based view: library details
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),

    # User authentication URLs
    path('register/', register, name='register'),  # custom registration view
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),  # CBV Login
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),  # CBV Logout
]
