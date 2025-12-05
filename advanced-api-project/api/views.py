from django.shortcuts import render
from rest_framework import generics, permissions
from .models import Book
from .serializers import BookSerializer


class BookListCreateView(generics.ListCreateAPIView):
    """
    Combined ListView and CreateView for Book.

    - GET  /api/books/   -> list all books
    - POST /api/books/   -> create a new book

    Uses:
    - queryset: all Book instances
    - serializer_class: BookSerializer
    - permission_classes: IsAuthenticatedOrReadOnly
      * Unauthenticated users: can only read (GET).
      * Authenticated users: can also create (POST).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        """
        Hook called by CreateAPIView when saving a new instance.

        This method is a good place to:
        - attach request.user as the creator/owner of the object
        - apply custom business rules before saving

        Here we simply call serializer.save(), but the method exists
        to demonstrate how to customize create behavior.
        """
        serializer.save()
        # Example of possible extension:
        # serializer.save(created_by=self.request.user)


class BookRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    Combined DetailView, UpdateView, and DeleteView for Book.

    - GET    /api/books/<pk>/ -> retrieve a single book
    - PUT    /api/books/<pk>/ -> full update
    - PATCH  /api/books/<pk>/ -> partial update
    - DELETE /api/books/<pk>/ -> delete the book

    Permissions:
    - Unauthenticated users: read-only (GET).
    - Authenticated users: can also update and delete (PUT/PATCH/DELETE).
    """
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        """
        Hook called when updating an existing instance.

        This is where you can:
        - enforce custom validation that depends on the current instance
        - log changes
        - modify data before saving

        Here we simply save the serializer.
        """
        serializer.save()

    def perform_destroy(self, instance):
        """
        Hook called when deleting an instance.

        You can override this to:
        - implement soft deletes
        - check related constraints
        - log who deleted what

        For now, we just call delete() on the instance.
        """
        instance.delete()

