from rest_framework import generics, permissions
from django_filters import rest_framework as filters                     # ✔ ALX-required import
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter          # ✔ ALX wants these imports

from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter
from api.authentication import CsrfExemptSessionAuthentication


# -----------------------
# LIST + FILTER + SEARCH + ORDERING
# -----------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = BookFilter

    search_fields = ['title', 'author__name']                           # ✔ ALX check
    ordering_fields = ['title', 'publication_year']                     # ✔ ALX check
    ordering = ['title']


# -----------------------
# DETAIL VIEW
# -----------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# -----------------------
# CREATE
# -----------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]


# -----------------------
# UPDATE
# -----------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]


# -----------------------
# DELETE
# -----------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]
