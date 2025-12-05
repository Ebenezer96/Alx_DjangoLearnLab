from django.urls import path

from .views import BookListCreateView, BookRetrieveUpdateDestroyView

urlpatterns = [
    # /api/books/  -> list all books (GET) and create new book (POST)
    path('books/', BookListCreateView.as_view(), name='book-list-create'),

    # /api/books/<pk>/  -> retrieve (GET), update (PUT/PATCH), delete (DELETE)
    path('books/<int:pk>/', BookRetrieveUpdateDestroyView.as_view(), name='book-detail'),
]
