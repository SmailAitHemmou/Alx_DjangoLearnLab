# relationship_app/urls.py
from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView 
from .views import admin_view, librarian_view, member_view

urlpatterns = [
    path("books/", views.list_books, name="list_books"),
    path("libraries/<int:pk>/", views.LibraryDetailView.as_view(), name="library_detail"),
    path('login/', LoginView.as_view(template_name='relationship_app/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='relationship_app/logout.html'), name='logout'),
    path('register/', views.register, name='register'),
    path('admin-page/', admin_view, name='admin-page'),
    path('librarian-page/', librarian_view, name='librarian-page'),
    path('member-page/', member_view, name='member-page'),
    path('books/add/', views.add_book, name='add_book'),
    path('books/<int:pk>/edit/', views.edit_book, name='edit_book'),
    path('books/<int:pk>/delete/', views.delete_book, name='delete_book'),  # Your registration function view
]
