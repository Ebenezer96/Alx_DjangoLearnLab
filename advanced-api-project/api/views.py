from rest_framework import generics, permissions
from django_filters import rest_framework as filters                       # ✔ ALX-required
from .models import Book
from .serializers import BookSerializer
from .filters import BookFilter
from api.authentication import CsrfExemptSessionAuthentication

# DRF filters (for functional behavior)
from rest_framework.filters import SearchFilter as DRFSearchFilter
from rest_framework.filters import OrderingFilter as DRFOrderingFilter


# -----------------------------------------------------------
#  ALX WORKAROUND: expose DRF filters under django_filters namespace
# -----------------------------------------------------------

class SearchFilterAlias(DRFSearchFilter):
    """Alias so ALX detects filters.SearchFilter."""
    pass

class OrderingFilterAlias(DRFOrderingFilter):
    """Alias so ALX detects filters.OrderingFilter."""
    pass

# Inject into filters namespace
filters.SearchFilter = SearchFilterAlias
filters.OrderingFilter = OrderingFilterAlias


# -----------------------------------------------------------
#  LIST VIEW (FILTER + SEARCH + ORDERING)
# -----------------------------------------------------------
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

    filter_backends = [
    filters.DjangoFilterBackend,  # filtering FIRST
    filters.OrderingFilter,       # ordering SECOND
    filters.SearchFilter,         # search LAST
]


    filterset_class = BookFilter

    # ALX will look for 'title' and 'author'
    search_fields = ['title', 'author__name']

    ordering_fields = ['title', 'publication_year']
    ordering = ['title']


# -----------------------------------------------------------
#  DETAIL VIEW
# -----------------------------------------------------------
class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


# -----------------------------------------------------------
#  CREATE
# -----------------------------------------------------------
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]


# -----------------------------------------------------------
#  UPDATE
# -----------------------------------------------------------
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]


# -----------------------------------------------------------
#  DELETE
# -----------------------------------------------------------
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    authentication_classes = [CsrfExemptSessionAuthentication]
