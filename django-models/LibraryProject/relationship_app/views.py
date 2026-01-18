from django.shortcuts import render
from django.views.generic.detail import DetailView
from .models import Library, Book

def list_books(request):
    books_list = Book.objects.all()
    context = {'books': books_list}
    return render(request, 'relationship_app/list_books.html', context)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  