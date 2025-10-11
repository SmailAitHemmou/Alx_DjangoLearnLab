from rest_framework import serializers
from .models import Post, Comment, Like

class CommentSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Comment
        fields = ['id', 'post', 'author', 'content', 'created_at', 'updated_at']
        read_only_fields = ['id', 'author', 'created_at', 'updated_at']


class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    comments = CommentSerializer(many=True, read_only=True)
    comments_count = serializers.IntegerField(source='comments.count', read_only=True)

    class Meta:
        model = Post
        fields = [
            'id', 'author', 'title', 'content',
            'comments_count', 'comments',
            'created_at', 'updated_at'
        ]
        read_only_fields = ['id', 'author', 'comments_count', 'comments', 'created_at', 'updated_at']


class LikeSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Like
        fields = ['id', 'post', 'user', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']