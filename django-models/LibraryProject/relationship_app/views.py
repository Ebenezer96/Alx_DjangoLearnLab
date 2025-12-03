from django.shortcuts import render
from django.http import HttpResponse
from .models import Book, Library
from django.views.generic import DetailView
from .models import Book

def list_books(request):
    """
    Function-based view that renders a list of all books
    and their authors using a template.
    """
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})



# Create your views here.
def list_books(request):
    """
    Function-based view that returns a simple text list
    of all books and their authors.
    """
    books = Book.objects.select_related('author').all()

    # Build a plain-text response
    lines = []
    for book in books:
        lines.append(f"{book.title} by {book.author.name}")

    response_text = "\n".join(lines) or "No books available."
    return HttpResponse(response_text, content_type="text/plain")

class LibraryDetailView(DetailView):
    """
    Class-based view to display details for a specific library,
    including all books available in that library.
    """
    model = Library
    template_name = "library_detail.html"   # we'll add this template (optional)
    context_object_name = "library"
    
    
def list_books(request):
    """
    Function-based view that renders a list of all books
    and their authors using a template.
    """
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})

