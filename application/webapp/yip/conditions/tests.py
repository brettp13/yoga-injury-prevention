import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from testing_utils import utils

from .models import Condition, ConditionCategory


class ListSelectConditions(APITestCase):
    def setUp(self):
        self.list_conditions_url = '/conditions/list-conditions/'
        self.select_condition_url = '/conditions/select-condition/'

        self.test_condition = Condition.objects.create(
            name='Epidimiosus', description='some shit with your knees')
        self.test_user = utils.create_test_user()
        self.token = Token.objects.get(user=self.test_user)

    def test_listing_conditions(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.get(self.list_conditions_url, format='json')
        utils.print_response_info(response, test_name='List Conditions Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_selecting_condition(self):
        data = {'condition_id': self.test_condition.id}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.select_condition_url, data, format='json')
        utils.print_response_info(response, test_name='Select Condition Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['name'], 'Epidimiosus')


class ListSelectConditionCategories(APITestCase):
    def setUp(self):
        self.list_condition_categories_url = '/conditions/list-condition-categories/'
        self.select_condition_category_url = '/conditions/select-condition-category/'

        self.test_condition_category = ConditionCategory.objects.create(
                name='Back Pain', description='When your back hurts'
        )
        self.test_user = utils.create_test_user()
        self.token = Token.objects.get(user=self.test_user)

    def test_listing_condition_categories(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.get(self.list_condition_categories_url, format='json')
        utils.print_response_info(response, test_name='List Conditions Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_selecting_condition_category(self):
        data = {'condition_category_id': self.test_condition_category.id}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.select_condition_category_url, data, format='json')
        utils.print_response_info(response, test_name='Select Condition Category Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['name'], 'Back Pain')

