from rest_framework import serializers
from .models import Author, Book
import datetime


# Serializer for the Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'publication_year', 'author']

    # Custom validation: publication year cannot be in the future
    def validate_publication_year(self, value):
        current_year = datetime.datetime.now().year
        if value > current_year:
            raise serializers.ValidationError("Publication year cannot be in the future.")
        return value
    
# BookSerializer:
# - Serializes all fields of the Book model
# - Adds validation so the publication_year is not in the future


# Serializer for the Author model
class AuthorSerializer(serializers.ModelSerializer):
    # Nest BookSerializer inside AuthorSerializer
    books = BookSerializer(many=True, read_only=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'books']

# AuthorSerializer:
# - Serializes the author's name
# - Includes nested books (via BookSerializer) using the related_name='books'
