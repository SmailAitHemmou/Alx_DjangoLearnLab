from django.shortcuts import render, redirect

# Create your views here.

# relationship_app/views.py
from django.http import HttpResponse
from django.views.generic.detail import DetailView
from .models import Library
from .models import Book
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404, redirect
from .forms import BookForm  # Make sure you have a BookForm for creating/editing

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
def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('book-list')  # redirect after registration
    else:
        form = UserCreationForm()
    return render(request, 'relationship_app/register.html', {'form': form})

# Check functions
def is_admin(user):
    return user.is_authenticated and user.userprofile.role == 'Admin'

def is_librarian(user):
    return user.is_authenticated and user.userprofile.role == 'Librarian'

def is_member(user):
    return user.is_authenticated and user.userprofile.role == 'Member'

# Role-based views
@user_passes_test(is_admin)
def admin_view(request):
    return render(request, 'relationship_app/admin_view.html')

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, 'relationship_app/librarian_view.html')

@user_passes_test(is_member)
def member_view(request):
    return render(request, 'relationship_app/member_view.html')


# Add Book view
@permission_required('relationship_app.can_add_book', raise_exception=True)
def add_book(request):
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Redirect to your book list page
    else:
        form = BookForm()
    return render(request, 'relationship_app/add_book.html', {'form': form})

# Edit Book view
@permission_required('relationship_app.can_change_book', raise_exception=True)
def edit_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'relationship_app/edit_book.html', {'form': form, 'book': book})

# Delete Book view
@permission_required('relationship_app.can_delete_book', raise_exception=True)
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.delete()
        return redirect('book_list')
    return render(request, 'relationship_app/delete_book.html', {'book': book})
