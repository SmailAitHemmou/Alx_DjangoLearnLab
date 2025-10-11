from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    target = serializers.SerializerMethodField()

    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target', 'unread', 'timestamp']

    def get_target(self, obj):
        if obj.target is None:
            return None
        # Minimal representation: "<ModelName: id>"
        return f'{obj.target.__class__.__name__}:{getattr(obj.target, "id", None)}'
