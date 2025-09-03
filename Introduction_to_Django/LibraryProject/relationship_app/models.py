from django.db import models

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books',
    )

    def __str__(self) -> str:
        return self.title


class Library(models.Model):
    name = models.CharField(max_length=200)
    books = models.ManyToManyField(
        Book,
        related_name='libraries',
        blank=True,
    )

    def __str__(self) -> str:
        return self.name


class Librarian(models.Model):
    name = models.CharField(max_length=200)
    library = models.OneToOneField(
        Library,
        on_delete=models.CASCADE,
        related_name='librarian',
    )

    def __str__(self) -> str:
        return f"{self.name} ({self.library.name})"
