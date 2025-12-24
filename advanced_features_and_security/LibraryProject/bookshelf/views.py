from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import permission_required
from .models import Book

"""
Permissions & Groups Setup:

Custom permissions are defined on the Book model:
- can_view
- can_create
- can_edit
- can_delete

Groups:
- Viewers: can_view
- Editors: can_view, can_create, can_edit
- Admins: all permissions

Permissions are enforced using Django's @permission_required decorator.
"""



@permission_required("bookshelf.can_view", raise_exception=True)
def book_list(request):
    books = Book.objects.all()
    return render(request, "bookshelf/book_list.html", {"books": books})


@permission_required("bookshelf.can_create", raise_exception=True)
def book_create(request):
    if request.method == "POST":
        title = request.POST["title"]
        author = request.POST["author"]
        year = request.POST["publication_year"]
        Book.objects.create(
            title=title,
            author=author,
            publication_year=year
        )
        return redirect("book_list")
    return render(request, "bookshelf/book_form.html")


@permission_required("bookshelf.can_edit", raise_exception=True)
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        book.title = request.POST["title"]
        book.author = request.POST["author"]
        book.publication_year = request.POST["publication_year"]
        book.save()
        return redirect("book_list")
    return render(request, "bookshelf/book_form.html", {"book": book})


@permission_required("bookshelf.can_delete", raise_exception=True)
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    book.delete()
    return redirect("book_list")
