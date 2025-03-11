from rest_framework.test import APIRequestFactory
from rest_framework import status
from django.test import TestCase
from .models import Post  # Import your Post model
from .views import PostListEndPoint  # Import your API view

class PostListAPITest(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = PostListEndPoint.as_view()
        self.url = "/api/posts/"  # Adjust to match your actual API URL

        # Create test data
        Post.objects.create(title="Post 1", content="Content 1")
        Post.objects.create(title="Post 2", content="Content 2")

    def test_get_post_list(self):
        request = self.factory.get(self.url)
        response = self.view(request)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # Expecting 2 posts
        self.assertEqual(response.data[0]["title"], "Post 1")
