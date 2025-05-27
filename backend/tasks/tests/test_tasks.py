from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from tasks.models import Task
from rest_framework_simplejwt.tokens import RefreshToken


class TaskAPITests(APITestCase):

    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password123')
        self.user2 = User.objects.create_user(username='otheruser', password='password123')

        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.access_token)

        self.task = Task.objects.create(user=self.user, title='Test Task')

        self.list_url = reverse('task-list-create')
        self.detail_url = lambda pk: reverse('task-detail', args=[pk])

    def test_create_task(self):
        data = {'title': 'New Task', 'description': 'Some description'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

    def test_list_tasks(self):
        Task.objects.create(user=self.user, title='Another Task')
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_retrieve_task(self):
        response = self.client.get(self.detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], self.task.title)

    def test_update_task(self):
        data = {'title': 'Updated Title', 'status': 'completed'}
        response = self.client.put(self.detail_url(self.task.id), data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, 'Updated Title')
        self.assertEqual(self.task.status, 'completed')
        self.assertIsNotNone(self.task.completed_at)

    def test_delete_task(self):
        response = self.client.delete(self.detail_url(self.task.id))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_access_without_authentication(self):
        self.client.credentials()  # remove token
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_user_cannot_access_others_tasks(self):
        task_other = Task.objects.create(user=self.user2, title='Other Task')
        response = self.client.get(self.detail_url(task_other.id))
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_task_with_empty_title(self):
        data = {'title': '  ', 'description': 'Invalid task'}
        response = self.client.post(self.list_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('title', response.data)
