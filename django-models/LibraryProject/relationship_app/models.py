from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Author(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    published_date = models.DateField()

    class Meta:
        permissions = (
            ("can_add_book", "Can add a book"),
            ("can_change_book", "Can edit a book"),
            ("can_delete_book", "Can delete a book"),
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

class UserProfile(models.Model):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Librarian', 'Librarian'),
        ('Member', 'Member'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)

    def __str__(self):
        return f"{self.user.username} - {self.role}"

# Automatically create or update the UserProfile when a User is saved
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance, role='Member')  # Default role is Member
    instance.userprofile.save()
