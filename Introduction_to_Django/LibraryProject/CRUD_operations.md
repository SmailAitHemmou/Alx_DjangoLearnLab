# CRUD Operations in Django Shell

This document demonstrates basic CRUD operations on the **Book** model in the `bookshelf` app using Django’s ORM.

---

## **1. Create a Book**

```python
from bookshelf.models import Book

# Create a new book
book = Book(title="1984", author="George Orwell", publication_year=1949)
book.save()  # Book instance saved

# Confirm creation
Book.objects.all()
