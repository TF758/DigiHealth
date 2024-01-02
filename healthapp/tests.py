from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import *

from django.conf import settings


# Create your tests here.


class TestLoginView(TestCase):
    def setUp(self):
        self.client = Client()
        self.registered_email = "test@test.com"
        self.unregistered_email = "test2@test.com"
        self.password = "password"
        self.user = get_user_model().objects.create_user(email=self.registered_email, password=self.password)

    def test_valid_login(self):
        """Testing that user can login with valid login credentials"""
        logged_in = self.client.login(email=self.registered_email, password=self.password)
        self.assertTrue(logged_in)


    def test_invalid_login(self):
        """Testing that invalid login credentials wont let user log in"""
        logged_in = self.client.login(email=self.unregistered_email, password=self.password)
        self.assertFalse(logged_in)


    def test_login_redirect(self):

        """Testing that accessing a login required page without logging will redirect user"""

        url = reverse('get_user_profile',kwargs={'email':self.registered_email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_can_access_by_login(self):

        """Testing that user can access page if logged in"""

        self.client.login(email=self.registered_email, password=self.password)
        url = reverse('get_user_profile',kwargs={'email':self.registered_email})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
    
        



#   def setUp(self): 
#         self.user = CustomUser.objects.create( email='test@email.com', password='')
#         self.user.set_password('secret')
#         self.user.save()
#         ...
#         self.client = Client()
#         self.client.login(username='testUser', password='secret')