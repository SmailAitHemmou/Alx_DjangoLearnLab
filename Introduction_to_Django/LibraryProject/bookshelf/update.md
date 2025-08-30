# Update Operation

```python
from bookshelf.models import Book

# Retrieve the book
b = Book.objects.get(title="1984")

# Update the title
b.title = "Nineteen Eighty-Four"
b.save()

# Confirm update
Book.objects.get(pk=b.pk).title