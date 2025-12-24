from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from django.db.models import Q

from .models import Book
from .forms import BookForm, BookSearchForm
from .forms import ExampleForm


@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    """
    SECURITY:
    - Uses Django ORM filters (parameterized) to prevent SQL injection.
    - Validates query input using BookSearchForm.
    - Relies on Django template auto-escaping to reduce XSS risks.
    """
    form = BookSearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        q = form.cleaned_data.get("q")
        if q:
            books = books.filter(Q(title__icontains=q) | Q(author__icontains=q))

    return render(request, "bookshelf/book_list.html", {"books": books, "form": form})


@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    """
    SECURITY:
    - Uses ModelForm validation rather than trusting raw POST data.
    - CSRF protection is enforced in the template via {% csrf_token %}.
    """
    if request.method == "POST":
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm()

    return render(request, "bookshelf/form_example.html", {"form": form})


@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    """
    SECURITY:
    - Uses ModelForm validation.
    - Avoids raw SQL and unvalidated input.
    """
    book = get_object_or_404(Book, pk=pk)

    if request.method == "POST":
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect("book_list")
    else:
        form = BookForm(instance=book)

    return render(request, "bookshelf/form_example.html", {"form": form, "book": book})


@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    """
    SECURITY:
    - Deletes via ORM only.
    - Permission gate prevents unauthorized deletion.
    """
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")
