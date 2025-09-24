from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


# List all books OR create a new book
class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: read is open, create requires authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# BookListCreateView:
# - GET /books/ : Returns list of all books
# - POST /books/ : Creates a new book (authenticated users only)


# Retrieve, update, or delete a book by ID
class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    # Permissions: read is open, update/delete requires authentication
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

# BookRetrieveUpdateDestroyView:
# - GET /books/<id>/ : Returns one book by ID
# - PUT/PATCH /books/<id>/ : Updates the book (authenticated users only)
# - DELETE /books/<id>/ : Deletes the book (authenticated users only)
