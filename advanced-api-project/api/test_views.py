from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase, APIClient

from .models import Author, Book

User = get_user_model()


class BookAPITests(APITestCase):
    """
    Tests for Book API endpoints:
    - List books (with filter/search/ordering)
    - Create book (authenticated only)
    - Retrieve single book
    - Update book (authenticated only)
    - Delete book (authenticated only)
    """

    @classmethod
    def setUpTestData(cls):
        # Create a user for authenticated tests
        cls.user = User.objects.create_user(username="testuser", password="testpass")

        # Create authors
        cls.author1 = Author.objects.create(name="Author One")
        cls.author2 = Author.objects.create(name="J.K. Rowling")

        # Create books (varied titles & years for filter/search/order tests)
        cls.book1 = Book.objects.create(title="Book One", publication_year=1997, author=cls.author1)
        cls.book2 = Book.objects.create(title="Harry Potter", publication_year=2000, author=cls.author2)
        cls.book3 = Book.objects.create(title="Newest Book", publication_year=2010, author=cls.author1)

    def setUp(self):
        # Use APIClient directly
        self.client = APIClient()

    # -------------------------
    # Basic list & detail tests
    # -------------------------
    def test_list_books(self):
        """GET /api/books/ should return all books (200)"""
        url = reverse('book-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # expect 3 books created in setUpTestData
        self.assertEqual(len(response.data), 3)

    def test_retrieve_book(self):
        """GET /api/books/<pk>/ should return the book detail"""
        url = reverse('book-detail', kwargs={'pk': self.book1.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.book1.title)

    # -------------------------
    # Create tests (permission)
    # -------------------------
    def test_create_book_unauthenticated_forbidden(self):
        """POST to create must be denied for unauthenticated users."""
        url = reverse('book-create')
        payload = {
            'title': 'Created Book',
            'publication_year': 2022,
            'author': self.author1.pk
        }
        response = self.client.post(url, payload, format='json')
        # Depending on auth setup this can be 401 or 403; ensure it is not allowed
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_create_book_authenticated(self):
        """Authenticated user can create a book (201) and DB reflects it."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-create')
        payload = {
            'title': 'Created Book',
            'publication_year': 2022,
            'author': self.author1.pk
        }
        response = self.client.post(url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        # Verify object was created in the DB
        self.assertTrue(Book.objects.filter(title='Created Book').exists())

    # -------------------------
    # Update tests (permission & data integrity)
    # -------------------------
    def test_update_book_unauthenticated_forbidden(self):
        """PATCH/PUT should be denied for unauthenticated users."""
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        response = self.client.patch(url, {'title': 'Hacked Title'}, format='json')
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_book_authenticated(self):
        """Authenticated user can update a book and DB is updated (200)."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-update', kwargs={'pk': self.book1.pk})
        response = self.client.patch(url, {'title': 'Updated Title'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, 'Updated Title')

    # -------------------------
    # Delete tests
    # -------------------------
    def test_delete_book_unauthenticated_forbidden(self):
        """DELETE should be denied for unauthenticated users."""
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        self.assertIn(response.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_delete_book_authenticated(self):
        """Authenticated user can delete a book (204) and it's removed from DB."""
        self.client.force_authenticate(user=self.user)
        url = reverse('book-delete', kwargs={'pk': self.book2.pk})
        response = self.client.delete(url)
        # Accept 204 No Content (typical) or 200 OK depending on view configuration
        self.assertIn(response.status_code, (status.HTTP_204_NO_CONTENT, status.HTTP_200_OK))
        self.assertFalse(Book.objects.filter(pk=self.book2.pk).exists())

    # -------------------------
    # Filtering / Search / Ordering tests
    # -------------------------
    def test_filter_by_publication_year(self):
        """Filtering: /api/books/?publication_year=<year> should return matching books only."""
        url = reverse('book-list') + f'?publication_year={self.book1.publication_year}'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for item in response.data:
            self.assertEqual(item['publication_year'], self.book1.publication_year)

    def test_search_by_title(self):
        """Search: /api/books/?search=Harry should return the 'Harry Potter' book."""
        url = reverse('book-list') + '?search=Harry'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Expect at least one result and one of them to be our book2
        titles = [item['title'] for item in response.data]
        self.assertIn(self.book2.title, titles)

    def test_ordering_by_publication_year_desc(self):
        """Ordering: /api/books/?ordering=-publication_year should return newest first."""
        url = reverse('book-list') + '?ordering=-publication_year'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [item['publication_year'] for item in response.data]
        # Verify the list is sorted descending by year
        self.assertEqual(years, sorted(years, reverse=True))
