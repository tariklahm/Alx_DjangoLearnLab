from rest_framework import serializers
from .models import Author, Book
import datetime

# Serializer for Book model
class BookSerializer(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation: year cannot be in the future
    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year

        if value > current_year:
            raise serializers.ValidationError(
                "Publication year cannot be in the future."
            )
        return value


# Serializer for Author with NESTED books
class AuthorSerializer(serializers.ModelSerializer):

    # Nested serializer to show author's books
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']
