from django.shortcuts import render

# Create your views here.

# relationship_app/views.py
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book

# --- Function-based view: list all books ---
def list_books(request):
    books = Book.objects.all()
    # OPTION A: return plain text (no template)
    # lines = [f"{b.title} by {b.author.name}" for b in books]
    # return HttpResponse("\n".join(lines), content_type="text/plain")

    # OPTION B: render a template (recommended)
    return render(request, "relationship_app/list_books.html", {"books": books})

# --- Class-based view: library detail + books in that library ---
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

    # Prefetch related books + authors for performance
    def get_queryset(self):
        return super().get_queryset().prefetch_related("books__author")

