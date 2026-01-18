from django.shortcuts import render
from django.views.generic.detail import DetailView
from bookshelf.models import Book, Library

def list_books(request):
    books_list = Book.objects.all()
    context = {'books': books_list}
    return render(request, 'relationship_app/list_books.html', context)
class LibraryDetailView(DetailView):
    model = Library
    template_name = 'relationship_app/library_detail.html'
    context_object_name = 'library'  # This is how you'll access the library in the template