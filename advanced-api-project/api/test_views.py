from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User

from .models import Book, Author


class BookAPITestCase(APITestCase):
        # ---------- READ TESTS (Unauthenticated allowed) ----------

    def test_list_books(self):
        """Unauthenticated users should be able to list all books."""
        response = self.client.get(self.list_url)

        # Should succeed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # We created 2 books in setUp()
        self.assertEqual(len(response.data), 2)

    def test_retrieve_book(self):
        """Unauthenticated users should be able to retrieve a single book."""
        response = self.client.get(self.detail_url)

        # Should succeed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verify returned book title is correct
        self.assertEqual(response.data["title"], "1984")
    # ---------- CREATE TESTS (Authentication required) ----------
        # ---------- CREATE TESTS ----------

    def test_create_book_requires_auth(self):
        """Anonymous users should NOT be able to create a book."""
        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id,
        }

        response = self.client.post(self.create_url, data)

        # Expected: 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_book_authenticated(self):
        """Authenticated users should be able to create a book."""
        # Log the user in
        self.client.login(username="testuser", password="testpassword")

        data = {
            "title": "New Book",
            "publication_year": 2020,
            "author": self.author.id,
        }

        response = self.client.post(self.create_url, data)

        # Expected: 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # There were originally 2 books → now there should be 3
        self.assertEqual(Book.objects.count(), 3)
    # ---------- UPDATE TESTS ----------

    def test_update_book_requires_auth(self):
        """Anonymous users should NOT be able to update a book."""
        data = {
            "title": "Updated Title",
            "publication_year": 1950,
            "author": self.author.id,
        }

        response = self.client.put(self.update_url, data)

        # Expected: 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_book_authenticated(self):
        """Authenticated users SHOULD be able to update a book."""
        # Log in user
        self.client.login(username="testuser", password="testpassword")

        data = {
            "title": "Updated Title",
            "publication_year": 1950,
            "author": self.author.id,
        }

        response = self.client.put(self.update_url, data)

        # Expected: 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Refresh book from database and verify the update
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.title, "Updated Title")

    pass
    def setUp(self):
        # API client for sending requests
        self.client = APIClient()

        # Create a test user for authenticated requests
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create an author
        self.author = Author.objects.create(name="George Orwell")

        # Create two books
        self.book1 = Book.objects.create(
            title="1984",
            publication_year=1949,
            author=self.author
        )
        self.book2 = Book.objects.create(
            title="Animal Farm",
            publication_year=1945,
            author=self.author
        )

        # URL names MUST match your api/urls.py
        self.list_url = reverse("book-list")
        self.detail_url = reverse("book-detail", kwargs={"pk": self.book1.id})
        self.create_url = reverse("book-create")
        self.update_url = reverse("book-update", kwargs={"pk": self.book1.id})
        self.delete_url = reverse("book-delete", kwargs={"pk": self.book1.id})
