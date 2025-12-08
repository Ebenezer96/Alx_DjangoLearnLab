from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase

from .models import Author, Book


class BookAPITestCase(APITestCase):
    """
    Tests for the Book API endpoints:
    - CRUD operations
    - filtering, searching, ordering
    - permissions / authentication
    """

    def setUp(self):
        # Test user for authenticated requests
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        # Authors
        self.author1 = Author.objects.create(name="J. K. Rowling")
        self.author2 = Author.objects.create(name="Robert C. Martin")

        # Books used across tests
        self.book1 = Book.objects.create(
            title="Harry Potter and the Goblet of Fire",
            publication_year=2000,
            author=self.author1,
        )
        self.book2 = Book.objects.create(
            title="Clean Code",
            publication_year=2008,
            author=self.author2,
        )
        self.book3 = Book.objects.create(
            title="The Clean Coder",
            publication_year=2011,
            author=self.author2,
        )

        # URL names must match api/urls.py
        self.list_url = reverse("book-list")
        self.create_url = reverse("book-create")
        self.detail_url = reverse("book-detail", args=[self.book1.pk])
        self.update_url = reverse("book-update", args=[self.book1.pk])
        self.delete_url = reverse("book-delete", args=[self.book1.pk])

    # ------------------------------------------------------------------
    # CRUD: LIST + DETAIL
    # ------------------------------------------------------------------

    def test_list_books_returns_all_books(self):
        """GET /api/books/ should return all books with 200 OK."""
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 3)
        titles = {b["title"] for b in response.data}
        self.assertIn(self.book1.title, titles)
        self.assertIn(self.book2.title, titles)
        self.assertIn(self.book3.title, titles)

    def test_retrieve_single_book(self):
        """GET /api/books/<id>/ should return the correct book."""
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.book1.id)
        self.assertEqual(response.data["title"], self.book1.title)

    # ------------------------------------------------------------------
    # CRUD: CREATE
    # ------------------------------------------------------------------

    def test_create_book_requires_authentication(self):
        """Unauthenticated POST should be rejected by permissions."""
        payload = {
            "title": "New Book",
            "publication_year": 2024,
            "author": self.author1.id,
        }
        response = self.client.post(self.create_url, payload, format="json")
        # Depending on configuration this may be 401 or 403; accept both
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    def test_create_book_authenticated(self):
        """Authenticated POST /books/create/ should create a new book."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Refactoring",
            "publication_year": 1999,
            "author": self.author2.id,
        }
        response = self.client.post(self.create_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.latest("id").title, "Refactoring")

    # ------------------------------------------------------------------
    # CRUD: UPDATE
    # ------------------------------------------------------------------

    def test_update_book_authenticated(self):
        """Authenticated PUT /books/update/<id>/ should update book fields."""
        self.client.force_authenticate(user=self.user)
        payload = {
            "title": "Harry Potter and the Goblet of Fire (Updated)",
            "publication_year": 2000,
            "author": self.author1.id,
        }
        response = self.client.put(self.update_url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book1.refresh_from_db()
        self.assertEqual(
            self.book1.title, "Harry Potter and the Goblet of Fire (Updated)"
        )

    def test_update_book_unauthenticated_forbidden(self):
        """Unauthenticated update should be blocked by permissions."""
        payload = {
            "title": "Should Not Work",
            "publication_year": 2000,
            "author": self.author1.id,
        }
        response = self.client.put(self.update_url, payload, format="json")
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )

    # ------------------------------------------------------------------
    # CRUD: DELETE
    # ------------------------------------------------------------------

    def test_delete_book_authenticated(self):
        """Authenticated DELETE /books/delete/<id>/ should remove the book."""
        self.client.force_authenticate(user=self.user)
        response = self.client.delete(self.delete_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(pk=self.book1.pk).exists())

    def test_delete_book_unauthenticated_forbidden(self):
        """Unauthenticated DELETE should be blocked by permissions."""
        response = self.client.delete(self.delete_url)
        self.assertIn(
            response.status_code,
            (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN),
        )
        self.assertTrue(Book.objects.filter(pk=self.book1.pk).exists())

    # ------------------------------------------------------------------
    # FILTERING: title, author, publication_year range
    # ------------------------------------------------------------------

    def test_filter_books_by_title(self):
        """Filter by title using ?title=clean should match both 'Clean' books."""
        url = self.list_url + "?title=clean"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertIn("Clean Code", titles)
        self.assertIn("The Clean Coder", titles)
        self.assertNotIn(self.book1.title, titles)

    def test_filter_books_by_author_name(self):
        """Filter by author name using ?author=martin should return only Martin's books."""
        url = self.list_url + "?author=martin"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        titles = {b["title"] for b in response.data}
        self.assertEqual(titles, {"Clean Code", "The Clean Coder"})

    def test_filter_books_by_publication_year_range(self):
        """Filter by min_year and max_year query params."""
        url = self.list_url + "?min_year=2005&max_year=2015"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertNotIn(self.book1.title, titles)  # 2000
        self.assertIn(self.book2.title, titles)     # 2008
        self.assertIn(self.book3.title, titles)     # 2011

    # ------------------------------------------------------------------
    # SEARCH: ?search=
    # ------------------------------------------------------------------

    def test_search_books_by_title(self):
        """Search by partial title using ?search=clean."""
        url = self.list_url + "?search=clean"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = {b["title"] for b in response.data}
        self.assertIn("Clean Code", titles)
        self.assertIn("The Clean Coder", titles)
        self.assertNotIn(self.book1.title, titles)

    def test_search_books_by_author_name(self):
        """Search by author name using ?search=rowling."""
        url = self.list_url + "?search=rowling"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.book1.title)

    # ------------------------------------------------------------------
    # ORDERING: ?ordering=
    # ------------------------------------------------------------------

    def test_order_books_by_title_ascending(self):
        """Ordering by title (?ordering=title) should sort alphabetically."""
        url = self.list_url + "?ordering=title"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [b["title"] for b in response.data]
        self.assertEqual(
            titles,
            sorted(titles),  # list must already be sorted asc by title
        )

    def test_order_books_by_publication_year_descending(self):
        """Ordering by -publication_year should return from newest to oldest."""
        url = self.list_url + "?ordering=-publication_year"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [b["publication_year"] for b in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
