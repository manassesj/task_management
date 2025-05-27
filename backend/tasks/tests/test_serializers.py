from django.test import TestCase
from django.utils import timezone
from rest_framework import serializers
from tasks.serializers import TaskCreateSerializer, TaskUpdateSerializer, TaskBaseSerializer
from tasks.models import Task
from django.contrib.auth.models import User

class TaskSerializerTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.task = Task.objects.create(user=self.user, title='Initial Task')

    def test_title_validation_empty(self):
        serializer = TaskBaseSerializer(data={'title': '   '})
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)
        self.assertEqual(serializer.errors['title'][0], "This field may not be blank.")

    def test_task_create_serializer_valid(self):
        data = {'title': 'New Task', 'description': 'Task description'}
        serializer = TaskCreateSerializer(data=data)
        self.assertTrue(serializer.is_valid())

        task = serializer.save(user=self.user)
        self.assertEqual(task.title, data['title'])
        self.assertEqual(task.description, data['description'])
        self.assertEqual(task.status, 'pending')

    def test_task_update_serializer_status_completed_sets_completed_at(self):
        serializer = TaskUpdateSerializer(instance=self.task, data={'title': 'Updated', 'status': 'completed'}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_task = serializer.save()
        self.assertEqual(updated_task.title, 'Updated')
        self.assertEqual(updated_task.status, 'completed')
        self.assertIsNotNone(updated_task.completed_at)
        self.assertTrue(timezone.now() - updated_task.completed_at < timezone.timedelta(seconds=2))

    def test_task_update_serializer_status_pending_clears_completed_at(self):
        self.task.status = 'completed'
        self.task.completed_at = timezone.now()
        self.task.save()

        serializer = TaskUpdateSerializer(instance=self.task, data={'title': 'Back to pending', 'status': 'pending'}, partial=True)
        self.assertTrue(serializer.is_valid())
        updated_task = serializer.save()
        self.assertEqual(updated_task.status, 'pending')
        self.assertIsNone(updated_task.completed_at)
