from django.shortcuts import render
from .models import Post
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from .forms import PostForm

# Create your views here.


def home(request):
    return render(request, "blog/home.html")
def home(request):
    posts = Post.objects.all().order_by('-published_date')
    return render(request, "blog/home.html", {'posts': posts})
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {'post': post})

def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("login")
    else:
        form = UserCreationForm()
    return render(request, "registration/signup.html", {"form": form})

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_form.html", {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=pk)  # Prevent editing others' posts

    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)

    return render(request, "blog/post_form.html", {"form": form})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if post.author != request.user:
        return redirect("post_detail", pk=pk)

    if request.method == "POST":
        post.delete()
        return redirect("home")

    return render(request, "blog/post_confirm_delete.html", {"post": post})
