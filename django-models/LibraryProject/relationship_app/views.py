from django.shortcuts import render
from django.http import HttpResponse
from .models import Book
from django.views.generic.detail import DetailView
from bookshelf.models import Library  # Adjust if your Library model is in another app
# Create your views here.

def book(request):
    books_list= Book.objects.all()
    book={'books':books_list}
    return render(request,'relationship_app/list_books.html' ,book)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  # This is how you'll access the library in the template