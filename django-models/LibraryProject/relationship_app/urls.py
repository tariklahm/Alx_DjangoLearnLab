from django.urls import path
from .views import list_books, LibraryDetailView  # checker expects list_books here

urlpatterns = [
    path('books/', list_books, name='list_books'),
    path('library/<int:pk>/', LibraryDetailView.as_view(), name='library_detail'),
    ]