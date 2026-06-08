import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from testing_utils import utils


class CreateAuthAccountTest(APITestCase):
    def setUp(self):
        self.url = '/auth/create-user/'
        self.email = utils.email_generator()
        self.username = self.email
        self.password = utils.password_generator()

    def test_create_account(self):
        data = [{'email': self.email, 'password': self.password}]
        response = self.client.post(self.url, data, format='json')
        utils.print_response_info(response, test_name='Create User Auth Test')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)[0]['email'], self.email)
        self.assertEqual(json.loads(response.content)[0]['username'], self.username)


class AuthSignInTest(APITestCase):
    """
    Make sure users can sign in
    """
    def setUp(self):
        self.url = '/auth/login/'
        self.password = utils.password_generator()
        self.test_user = utils.create_test_user(password=self.password)
        self.token = Token.objects.get(user=self.test_user)

    def test_login(self):
        data = {'email': self.test_user.email, 'password': self.password}
        response = self.client.post(self.url, data, format='json')
        utils.print_response_info(response, test_name='Auth SignIn Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['token'], self.token.key)


class EditAuthAccountTest(APITestCase):
    """
    Make sure it is possible to edit account email / password
    """
    def setUp(self):
        self.url = '/auth/user-detail/'
        self.test_user = utils.create_test_user()
        self.token = Token.objects.get(user=self.test_user)

    def test_edit_account_email(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {'email': 'new-email-value@gmail.com'}
        response = self.client.put(self.url, data, format='json')
        utils.print_response_info(response, test_name='Edit Auth Account Email Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['email'], 'new-email-value@gmail.com')

    def test_edit_account_password(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {'password': 'new-password-value'}
        response = self.client.put(self.url, data, format='json')
        utils.print_response_info(response, test_name='Edit Auth Account Password Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
