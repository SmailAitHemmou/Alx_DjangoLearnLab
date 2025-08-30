# Delete Operation

```python
from bookshelf.models import Book

# Retrieve the book
b = Book.objects.get(title="Nineteen Eighty-Four")

# Delete the book
b.delete()

# Confirm deletion
Book.objects.all()