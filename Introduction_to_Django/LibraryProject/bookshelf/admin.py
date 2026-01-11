from django.contrib import admin
from .models import Book

# Custom admin class
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'publication_year')  # Columns to display in list view
    search_fields = ('title', 'author')  # Allow searching by title or author
    list_filter = ('publication_year',)  # Add filter by publication year

# Register Book with custom admin
admin.site.register(Book, BookAdmin)