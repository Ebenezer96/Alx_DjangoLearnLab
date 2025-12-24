from relationship_app.models import Author, Book, Library, Librarian

# 1. Query all books by a specific author
def get_books_by_author(author_name):
    """
    Returns a queryset of all Book objects written by an author
    with the given name.
    """
    author = Author.objects.get(name=author_name)
    return Book.objects.filter(author=author)


# 2. List all books in a library
def get_books_in_library(library_name):
    """
    Returns a queryset of all Book objects that belong
    to the Library with the given name.
    """
    library = Library.objects.get(name=library_name)
    return library.books.all()


# 3. Retrieve the librarian for a library
def get_librarian_for_library(library_name):
    """
    Returns the Librarian object for the Library
    with the given name.
    """
    library = Library.objects.get(name=library_name)
    librarian = Librarian.objects.get(library=library)
    return librarian
