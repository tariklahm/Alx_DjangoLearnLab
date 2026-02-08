from django.db import models

# Author model represents a writer who can have multiple books
class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


# Book model represents books written by authors
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()

    # One Author → Many Books relationship
    author = models.ForeignKey(
        Author,
        related_name='books',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.title
