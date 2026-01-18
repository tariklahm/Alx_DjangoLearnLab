
from .models import Author,Book,Library,Librarian




    
#Query all books by a specific author.
author=Author.objects.get(id=1)
books=author.books.all()


#List all books in a library.
library=Library.objects.get(id=1)
books=library.books.all()

#Retrieve the librarian for a library.
library=Library.objects.get(id=1)
librarian=library.librarian