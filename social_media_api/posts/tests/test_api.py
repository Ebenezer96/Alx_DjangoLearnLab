from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from posts.models import Post

User = get_user_model()


class TestPostAPI(APITestCase):

    def authenticate(self, user):
        """
        Attach JWT credentials to the test client.
        """
        refresh = RefreshToken.for_user(user)
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}"
        )

    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser",
            password="password123"
        )

    def test_public_can_list_posts(self):
        response = self.client.get("/api/posts/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_authenticated_user_can_create_post(self):
        self.authenticate(self.user)

        response = self.client.post(
            "/api/posts/",
            {"title": "JWT Post", "content": "JWT works"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["author"], "testuser")

    def test_user_cannot_edit_others_post(self):
        other = User.objects.create_user(
            username="other",
            password="password123"
        )

        post = Post.objects.create(
            author=other,
            title="Other post",
            content="No access",
        )

        self.authenticate(self.user)

        response = self.client.patch(
            f"/api/posts/{post.id}/",
            {"title": "Hacked"},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
