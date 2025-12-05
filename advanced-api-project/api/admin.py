from django.contrib import admin

from .models import Author, Book


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Author model.

    Allows easy creation and inspection of Author instances
    via Django admin.
    """
    list_display = ('id', 'name')
    search_fields = ('name',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    """
    Admin configuration for the Book model.

    Shows a basic list of books and their related authors,
    making it easy to verify database contents during development.
    """
    list_display = ('id', 'title', 'publication_year', 'author')
    list_filter = ('publication_year', 'author')
    search_fields = ('title',)
