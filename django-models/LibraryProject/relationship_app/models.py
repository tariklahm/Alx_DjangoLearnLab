from django.db import models


#Author Model:
class Author(models.Model):
    name=models.CharField(max_length=50)
#Book Model:
class Book(models.Model):
    title=models.CharField(max_length=50)
    author=models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
#Library Model:
class Library(models.Model):
    name=models.CharField(max_length=50)
    books=models.ManyToManyField(Book, related_name='libraries')
#Librarian Model:
class Librarian(models.Model):
    name=models.CharField(max_length=50)
    library=models.OneToOneField(Library, on_delete=models.CASCADE, related_name='librarian')