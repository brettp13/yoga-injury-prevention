import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from testing_utils import utils

from .models import YogaStyle


class CreateProfile(APITestCase):
    def setUp(self):
        self.url = '/profile/create-profile/'
        self.test_auth = utils.create_test_user()
        self.token = Token.objects.get(user=self.test_auth)
        YogaStyle.objects.create(title='Iyengar', public=True)

    def test_create_user_profile(self):
        data = {
                'first_name': 'Taliesin',
                'last_name': 'Oppenheimer',
                'country': 'MEX',
                'region': 'Ciudad De Mexico',
                'city': 'CDMX',
                'state': '',
                'postal_code': '06700',
                'street': 'Guanajuato 181 Roma Nte',
                'yoga_style': '1',
                'is_teacher': 'False',
        }
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.url, data, format='json')
        utils.print_response_info(response, test_name='Create Profile Test')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)



class ProfileDetail(APITestCase):
    def setUp(self):
        self.url='/profile/profile-detail/'
        test_user = utils.create_test_user()
        self.test_user_profile = utils.create_test_user_profile(user=test_user)
        self.token = Token.objects.get(user=test_user)
        self.yoga_style = YogaStyle.objects.create(title='Iyengar', public=True)

    def test_edit_user_profile(self):
        data = {'yoga_style': str(self.yoga_style.id)}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.put(self.url, data, format='json')
        utils.print_response_info(response, test_name='Edit User Profile Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['yoga_style'], 'Iyengar')


    def test_delete_user_profile(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.delete(self.url, format='json')
        utils.print_response_info(response, test_name='Delete User Profile Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListCreateYogaStyle(APITestCase):
    def setUp(self):
        self.list_yoga_styles_url = '/profile/list-yoga-styles/'
        self.create_yoga_style_url = '/profile/create-yoga-style/'
        yoga_style_1 = utils.create_test_yoga_style()
        yoga_style_2 = utils.create_test_yoga_style()

    def test_list_yoga_styles(self):
        response = self.client.get(self.list_yoga_styles_url, format='json')
        utils.print_response_info(response, test_name='List Yoga Styles Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_yoga_style(self):
        data = {'title': 'My Personal Style', 'public': False}
        response = self.client.post(self.create_yoga_style_url, data, format='json')
        utils.print_response_info(response, test_name='Create Yoga Style Test')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(json.loads(response.content)['title'], 'My Personal Style')


