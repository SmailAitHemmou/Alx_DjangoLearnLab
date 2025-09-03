# Retrieve Operation

```python
from bookshelf.models import Book

# Retrieve the book by title
b = Book.objects.get(title="1984")
print(b.title, b.author, b.publication_year)