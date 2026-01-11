from bookshelf.models import Book

# delete book
book.delete()   #expected output: (1, {'bookshelf.Book': 1})

# verify that the book is deleted
Book.objects.all()  #expected output : <QuerySet []>