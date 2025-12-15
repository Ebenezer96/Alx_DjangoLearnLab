from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from posts.models import Post, Like
from notifications.models import Notification

User = get_user_model()


class TestLikesAndNotifications(APITestCase):
    def setUp(self):
        self.author = User.objects.create_user(
            username="author",
            password="password123"
        )
        self.liker = User.objects.create_user(
            username="liker",
            password="password123"
        )

        self.post = Post.objects.create(
            author=self.author,
            title="Test post",
            content="Test content",
        )

    def authenticate(self, user):
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def test_like_creates_like_and_notification(self):
        self.authenticate(self.liker)

        response = self.client.post(
            f"/api/posts/{self.post.id}/like/"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Like.objects.count(), 1)

        notification = Notification.objects.first()
        self.assertIsNotNone(notification)
        self.assertEqual(notification.recipient, self.author)
        self.assertEqual(notification.actor, self.liker)
        self.assertIn("liked", notification.verb)

    def test_user_cannot_like_same_post_twice(self):
        self.authenticate(self.liker)

        self.client.post(f"/api/posts/{self.post.id}/like/")
        response = self.client.post(f"/api/posts/{self.post.id}/like/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Like.objects.count(), 1)

    def test_unlike_removes_like(self):
        self.authenticate(self.liker)

        self.client.post(f"/api/posts/{self.post.id}/like/")
        response = self.client.post(f"/api/posts/{self.post.id}/unlike/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Like.objects.count(), 0)

    def test_author_can_view_notifications(self):
        self.authenticate(self.liker)
        self.client.post(f"/api/posts/{self.post.id}/like/")

        self.authenticate(self.author)
        response = self.client.get("/api/notifications/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
