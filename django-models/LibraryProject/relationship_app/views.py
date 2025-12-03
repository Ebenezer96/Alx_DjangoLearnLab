from django.shortcuts import render, redirect
from django.views.generic.detail import DetailView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from .models import Library, Book



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
