from django.shortcuts import render, redirect

# Create your views here.

# relationship_app/views.py
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required


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
    
# LOGIN VIEW
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('book-list')  # redirect after login
    else:
        form = AuthenticationForm()
    return render(request, 'relationship_app/login.html', {'form': form})

# LOGOUT VIEW
@login_required
def logout_view(request):
    logout(request)
    return render(request, 'relationship_app/logout.html')

# REGISTRATION VIEW
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-list')  # redirect after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})
