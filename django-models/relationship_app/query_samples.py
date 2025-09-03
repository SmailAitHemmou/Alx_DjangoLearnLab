"""
Run with:
    python relationship_app/query_samples.py

This script auto-detects your Django settings module, then runs the sample queries:
- Query all books by a specific author.
- List all books in a library.
- Retrieve the librarian for a library.
"""

from pathlib import Path
import os
import sys

# === Locate project root (folder that contains manage.py) ===
BASE_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE_DIR))

# === Try to guess the settings module if DJANGO_SETTINGS_MODULE not set ===
def _guess_settings_module():
    for p in BASE_DIR.iterdir():
        # Look for a package that has settings.py (e.g., auth_project/settings.py)
        if p.is_dir() and (p / "__init__.py").exists() and (p / "settings.py").exists():
            return f"{p.name}.settings"
    return None

os.environ.setdefault(
    "DJANGO_SETTINGS_MODULE",
    os.environ.get("DJANGO_SETTINGS_MODULE") or _guess_settings_module() or "auth_project.settings"
)

import django  # noqa: E402
django.setup()

from relationship_app.models import Author, Book, Library, Librarian  # noqa: E402


def books_by_author(author_name: str):
    """Return queryset of books for the given author name."""
    return Book.objects.filter(author__name=author_name).only("id", "title").order_by("title")


def books_in_library(library_name: str):
    """Return queryset of books that belong to a given library name."""
    return Book.objects.filter(libraries__name=library_name).only("id", "title").order_by("title")


def librarian_for_library(library_name: str):
    """Return the librarian instance for a given library name, or None."""
    return Librarian.objects.filter(library__name=library_name).select_related("library").first()


def print_header(title: str):
    print("\n" + "=" * 80)
    print(title)
    print("=" * 80)


def main():
    # 1) Query all books by a specific author
    author_name = "George Orwell"
    print_header(f'Books by author: "{author_name}"')
    for b in books_by_author(author_name):
        print(f"- {b.title}")

    # 2) List all books in a library
    lib_name = "Central Library"
    print_header(f'Books in library: "{lib_name}"')
    for b in books_in_library(lib_name):
        print(f"- {b.title}")

    # 3) Retrieve the librarian for a library
    lib_name2 = "West Branch"
    print_header(f'Librarian for library: "{lib_name2}"')
    librarian = librarian_for_library(lib_name2)
    if librarian:
        print(f"- {librarian.name} (manages {librarian.library.name})")
    else:
        print("- No librarian found")

    print("\nDone.")


if __name__ == "__main__":
    main()
