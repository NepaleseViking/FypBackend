from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse

class LoginTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.username = 'testuser'
        self.password = 'testpass123'
        User.objects.create_user(username=self.username, password=self.password)

    def test_login_with_valid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': self.password
        })
        self.assertEqual(response.status_code, 302)  # typically a redirect on success

    def test_login_with_invalid_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': self.username,
            'password': 'wrongpass'
        })
        self.assertNotEqual(response.status_code, 302)
        self.assertContains(response, "invalid", status_code=200)  # adjust based on your template
