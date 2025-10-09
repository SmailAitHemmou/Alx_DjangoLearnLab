from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class PostCommentTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='bob', password='pw12345')
        self.token = Token.objects.create(user=self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_create_post_and_comment(self):
        # create post
        resp = self.client.post('/api/posts/', {'title': 't', 'content': 'c'}, format='json')
        assert resp.status_code == 201
        post_id = resp.data['id']

        # create comment
        resp2 = self.client.post('/api/comments/', {'post': post_id, 'content': 'nice'}, format='json')
        assert resp2.status_code == 201
        assert resp2.data['author'] == self.user.username
