from django.test import TestCase
from django.contrib.auth.models import User
from users.serializers import RegisterSerializer

class RegisterSerializerTests(TestCase):

    def setUp(self):
        User.objects.create_user(username='existinguser', password='password123')

    def test_valid_data_creates_user(self):
        data = {
            'username': 'newuser',
            'password': 'password123',
            'password2': 'password123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        user = serializer.save()
        self.assertEqual(user.username, 'newuser')
        self.assertTrue(user.check_password('password123'))

    def test_username_already_taken(self):
        data = {
            'username': 'existinguser',
            'password': 'password123',
            'password2': 'password123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('username', serializer.errors)
        self.assertEqual(serializer.errors['username'][0], 'A user with that username already exists.')

    def test_password_too_short(self):
        data = {
            'username': 'shortpassuser',
            'password': '123',
            'password2': '123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], 'Password must be at least 8 characters long.')

    def test_passwords_do_not_match(self):
        data = {
            'username': 'newuser2',
            'password': 'password123',
            'password2': 'different123'
        }
        serializer = RegisterSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('password', serializer.errors)
        self.assertEqual(serializer.errors['password'][0], "Password fields didn't match.")
