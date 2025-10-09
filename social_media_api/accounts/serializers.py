from rest_framework import serializers
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    token = serializers.SerializerMethodField(read_only=True)
    profile_picture = serializers.ImageField(required=False, allow_null=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'bio', 'profile_picture', 'token')
        read_only_fields = ('id', 'token')

    def get_token(self, obj):
        token, _ = Token.objects.get_or_create(user=obj)
        return token.key

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
