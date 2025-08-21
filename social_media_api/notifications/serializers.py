from rest_framework import serializers
from .models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    class Meta:
        model = Notification
        fields = ['id', 'recipient', 'actor', 'verb', 'target_object_id', 'timestamp', 'unread']
