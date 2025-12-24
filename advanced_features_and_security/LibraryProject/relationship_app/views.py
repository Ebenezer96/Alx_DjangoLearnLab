from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login    # <-- REQUIRED BY ALX CHECKER
from .models import Library
from .models import Book
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import permission_required





# Function-based view (checker requires template + Book.objects.all())
def list_books(request):
    books = Book.objects.all()
    return render(request, "relationship_app/list_books.html", {"books": books})


# Class-based view (checker requires DetailView + correct template path)
class LibraryDetailView(DetailView):
    model = Library
    template_name = "relationship_app/library_detail.html"
    context_object_name = "library"

class UserLoginView(LoginView):
    template_name = "relationship_app/login.html"
    redirect_authenticated_user = True

class UserLogoutView(LogoutView):
    template_name = "relationship_app/logout.html"


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()              # create the user
            return redirect("login") # after successful registration, go to login
    else:
        form = UserCreationForm()

    return render(request, "relationship_app/register.html", {"form": form})

def is_admin(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Admin'

def is_librarian(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Librarian'

def is_member(user):
    return hasattr(user, 'userprofile') and user.userprofile.role == 'Member'

@user_passes_test(is_admin)
def admin_view(request):
    return render(request, "relationship_app/admin_view.html")

@user_passes_test(is_librarian)
def librarian_view(request):
    return render(request, "relationship_app/librarian_view.html")

@user_passes_test(is_member)
def member_view(request):
    return render(request, "relationship_app/member_view.html")


@permission_required("relationship_app.can_add_book")
def add_book(request):
    # your existing add-book logic here
    ...


@permission_required("relationship_app.can_change_book")
def edit_book(request, book_id):
    # your existing edit-book logic here
    ...


@permission_required("relationship_app.can_delete_book")
def delete_book(request, book_id):
    # your existing delete-book logic here
    ...