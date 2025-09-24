from django.db import models

# Author model represents a book author
class Author(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

# Author model:
# - Represents a writer with a name
# - Related to multiple books (one-to-many relationship)


# Book model represents a book written by an author
class Book(models.Model):
    title = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    author = models.ForeignKey(
        Author,
        related_name='books',   # allows accessing books via author.books
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.title} ({self.publication_year})"
    
# Book model:
# - Represents a book with a title and publication year
# - Has a ForeignKey to Author (each book belongs to one author)

