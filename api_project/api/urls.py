from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BookList, BookViewSet

# Router for ViewSet-based CRUD endpoints
router = DefaultRouter()
router.register(r'books_all', BookViewSet, basename='book_all')

urlpatterns = [
    # Public list endpoint using generic ListAPIView
    path('books/', BookList.as_view(), name='book-list'),

    # Include all ViewSet-generated routes (requires authentication)
    path('', include(router.urls)),
]
