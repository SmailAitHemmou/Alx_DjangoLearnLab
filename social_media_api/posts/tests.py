from django.test import TestCase
from rest_framework.test import APITestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token
from posts.models import Post, Like

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


class LikeNotificationTest(APITestCase):
    def setUp(self):
        self.a = User.objects.create_user(username='a', password='pw')
        self.b = User.objects.create_user(username='b', password='pw')
        self.post = Post.objects.create(author=self.b, title='t', content='c')
        self.token = Token.objects.create(user=self.a)
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token.key}')

    def test_like_creates_notification(self):
        resp = self.client.post(f'/api/posts/{self.post.id}/like/')
        assert resp.status_code == 201
        # check like exists
        assert Like.objects.filter(post=self.post, user=self.a).exists()
        # b should have a notification
        self.assertEqual(self.b.notifications.count(), 1)
