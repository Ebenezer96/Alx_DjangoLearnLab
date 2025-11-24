import django
import os

# Adjust project name if needed
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "django_models.settings")
django.setup()

from relationship_app.models import Author, Book, Library


# 1. Query all books by a specific author
def query_books_by_author(author_name):
    author = Author.objects.filter(name=author_name).first()
    if not author:
        print("Author not found.")
        return
    books = author.books.all()
    print(f"Books by {author_name}:")
    for book in books:
        print(f"- {book.title}")


# 2. List all books in a library
def list_books_in_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if not library:
        print("Library not found.")
        return
    print(f"Books in {library_name}:")
    for book in library.books.all():
        print(f"- {book.title}")


# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    library = Library.objects.filter(name=library_name).first()
    if not library:
        print("Library not found.")
        return
    librarian = getattr(library, "librarian", None)
    if librarian:
        print(f"Librarian for {library_name}: {librarian.name}")
    else:
        print("No librarian assigned.")


# test calls
if __name__ == "__main__":
    query_books_by_author("John Doe")
    list_books_in_library("Central Library")
    get_librarian_for_library("Central Library")
