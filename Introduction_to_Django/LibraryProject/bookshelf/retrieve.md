from bookshelf.models import Book

# Retrieve the book with title "1984"
book = Book.objects.get(title="1984")

# Display all its attributes
print(book.title, book.author, book.publication_year)  

# Expected output: 1984 George Orwell 1949