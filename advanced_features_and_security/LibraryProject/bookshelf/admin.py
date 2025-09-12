from django.contrib import admin

from LibraryProject.accounts.admin import CustomUserAdmin
from .models import CustomUser
# Register your models here.

from .models import Book

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # columns shown in the list page
    list_display = ("title", "author", "published_date")
    # right-side filters
    list_filter = ("author", "published_date")
    # top search box
    search_fields = ("title", "author")
    # optional niceties
    ordering = ("title",)
    list_per_page = 25

    admin.site.register(CustomUser, CustomUserAdmin)