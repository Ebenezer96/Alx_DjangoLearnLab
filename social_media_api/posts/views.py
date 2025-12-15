from rest_framework import viewsets, permissions, filters, generics
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.contenttypes.models import ContentType

from .models import Post, Comment, Like
from .serializers import PostSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly
from notifications.models import Notification


#PostViewSet
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
        )

        if not created:
            return Response(
                {"detail": "You have already liked this post."},
                status=400,
            )

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

        return Response(
            {"detail": "Post liked successfully."},
            status=201,
        )

#CommentViewSet
class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
        )

        if not created:
            return Response(
                {"detail": "You have already liked this post."},
                status=400,
            )

        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

        return Response(
            {"detail": "Post liked successfully."},
            status=201,
        )

#Class FeedView      
class FeedView(generics.ListAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        following_users = self.request.user.following.all()
        return Post.objects.filter(author__in=following_users).order_by("-created_at")

class LikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)

        like, created = Like.objects.get_or_create(
            user=request.user,
            post=post,
        )

        if not created:
            return Response(
                {"detail": "You have already liked this post."},
                status=400,
            )
# Create notification for post author
        if post.author != request.user:
            Notification.objects.create(
                recipient=post.author,
                actor=request.user,
                verb="liked your post",
                target_content_type=ContentType.objects.get_for_model(post),
                target_object_id=post.id,
            )

        return Response(
            {"detail": "Post liked successfully."},
            status=201,
        )

#unlike view
class UnlikePostView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        post = generics.get_object_or_404(Post, pk=pk)

        like = Like.objects.filter(
            user=request.user,
            post=post,
        ).first()

        if not like:
            return Response(
                {"detail": "You have not liked this post."},
                status=400,
            )

        like.delete()
        return Response(
            {"detail": "Post unliked successfully."},
            status=200,
        )
