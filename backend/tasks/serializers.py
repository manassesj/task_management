from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'completed_at', 'status']

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("Title cannot be empty.")
        return value


class TaskCreateSerializer(TaskBaseSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description']


class TaskUpdateSerializer(TaskBaseSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'status']

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        status = validated_data.get('status', instance.status)

        if status != instance.status:
            instance.status = status
            if status == 'completed':
                instance.completed_at = timezone.now()
            elif status == 'pending':
                instance.completed_at = None

        instance.save()
        return instance


class TaskDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'title', 'description', 'created_at', 'completed_at', 'status']
