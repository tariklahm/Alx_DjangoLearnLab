
from .models import Author,Book,Library,Librarian

# Query all books by a specific author
author = Author.objects.get(id=1)
books_by_author = author.books.all()

# List all books in a library (by name)
library_name = "Central Library"  
library = Library.objects.get(name=library_name)
books_in_library = library.books.all()

# Retrieve the librarian for a library (by name)
librarian = library.librarian