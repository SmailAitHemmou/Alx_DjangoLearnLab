from django.shortcuts import render

# Create your views here.
from rest_framework import viewsets
from rest_framework import generics
from .models import Book
from .serializers import BookSerializer

class BookList(generics.ListAPIView):
    """
    GET /api/books/  -> returns list of all books
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer

# ViewSet for CRUD operations
class BookViewSet(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer