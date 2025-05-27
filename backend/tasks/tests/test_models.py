from django.test import TestCase
from django.contrib.auth.models import User
from tasks.models import Task
from django.utils import timezone
import datetime

class TaskModelTests(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')

    def test_create_task_defaults(self):
        task = Task.objects.create(user=self.user, title='Test Task')
        self.assertEqual(task.status, 'pending')
        self.assertIsNone(task.completed_at)
        self.assertEqual(str(task), 'Test Task')
        self.assertIsNotNone(task.created_at)

    def test_save_sets_completed_at_when_status_completed(self):
        task = Task.objects.create(user=self.user, title='Complete me', status='pending')
        self.assertIsNone(task.completed_at)

        task.status = 'completed'
        task.save()

        self.assertIsNotNone(task.completed_at)
        self.assertTrue(timezone.now() - task.completed_at < datetime.timedelta(seconds=2))

    def test_save_clears_completed_at_when_status_pending(self):
        task = Task.objects.create(user=self.user, title='Pending Task', status='completed')
        self.assertIsNotNone(task.completed_at)

        task.status = 'pending'
        task.save()

        self.assertIsNone(task.completed_at)
