from django.urls import path
from .views import (
    PostListView,
    PostDetailView,
    PostCreateView,
    PostUpdateView,
    PostDeleteView,
    CommentCreateView,
    CommentUpdateView,
    CommentDeleteView,
)

urlpatterns = [
    # Post CRUD
    path("post/", PostListView.as_view(), name="post-list"),
    path("post/new/", PostCreateView.as_view(), name="post-new"),
    path("post/<int:pk>/", PostDetailView.as_view(), name="post-detail"),
    path("post/<int:pk>/update/", PostUpdateView.as_view(), name="post-update"),
    path("post/<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),

    # Comment CRUD (CHECKER-REQUIRED PATTERN)
    path(
        "post/<int:pk>/comments/new/",
        CommentCreateView.as_view(),
        name="comment-create",
    ),

    path(
        "comment/<int:pk>/update/",
        CommentUpdateView.as_view(),
        name="comment-update",
    ),
    path(
        "comment/<int:pk>/delete/",
        CommentDeleteView.as_view(),
        name="comment-delete",
    ),
]
