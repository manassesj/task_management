from django.test import TestCase, RequestFactory
from django.contrib.auth.models import User
from rest_framework.test import APIRequestFactory
from tasks.permissions import IsOwner
from tasks.models import Task

class IsOwnerPermissionTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.permission = IsOwner()

        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')

        self.task_user1 = Task.objects.create(user=self.user1, title='Task User 1')
        self.task_user2 = Task.objects.create(user=self.user2, title='Task User 2')

    def test_permission_granted_to_owner(self):
        request = self.factory.get('/fake-url/')
        request.user = self.user1

        self.assertTrue(self.permission.has_object_permission(request, None, self.task_user1))

    def test_permission_denied_to_non_owner(self):
        request = self.factory.get('/fake-url/')
        request.user = self.user1

        self.assertFalse(self.permission.has_object_permission(request, None, self.task_user2))
