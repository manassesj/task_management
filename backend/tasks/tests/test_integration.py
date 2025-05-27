from rest_framework.test import APITestCase, APIClient
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from tasks.models import Task

class TaskIntegrationTests(APITestCase):
    def setUp(self):
        self.client = APIClient()
        self.register_url = reverse('register')
        self.login_url = reverse('login')
        self.tasks_url = reverse('task-list-create') 

        self.user_data = {'username': 'user1', 'password': 'password123', 'password2': 'password123'}
        self.client.post(self.register_url, self.user_data, format='json')

        response = self.client.post(self.login_url, {'username': 'user1', 'password': 'password123'}, format='json')
        self.token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    def test_create_task(self):
        data = {'title': 'Test Task', 'description': 'Testing task creation'}
        response = self.client.post(self.tasks_url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 1)
        self.assertEqual(Task.objects.first().title, 'Test Task')

    def test_list_tasks(self):
        Task.objects.create(user=User.objects.get(username='user1'), title='Task 1')

        response = self.client.get(self.tasks_url, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_update_task_status(self):
        task = Task.objects.create(user=User.objects.get(username='user1'), title='Task Update')

        update_url = reverse('task-detail', args=[task.id])
        data = {'title': 'Task Updated', 'status': 'completed'}
        response = self.client.put(update_url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        updated_task = Task.objects.get(id=task.id)
        self.assertEqual(updated_task.status, 'completed')
        self.assertIsNotNone(updated_task.completed_at)

    def test_delete_task(self):
        task = Task.objects.create(user=User.objects.get(username='user1'), title='Task Delete')

        delete_url = reverse('task-detail', args=[task.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Task.objects.count(), 0)

    def test_task_owner_protection(self):
        task = Task.objects.create(user=User.objects.get(username='user1'), title='Private Task')

        self.client.post(self.register_url, {'username': 'user2', 'password': 'password123', 'password2': 'password123'}, format='json')
        login_response = self.client.post(self.login_url, {'username': 'user2', 'password': 'password123'}, format='json')
        token2 = login_response.data['access']

        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token2}')

        delete_url = reverse('task-detail', args=[task.id])
        response = self.client.delete(delete_url)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
