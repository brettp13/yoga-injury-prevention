import json

from rest_framework import status
from rest_framework.test import APITestCase

from testing_utils import utils

from .models import AcknowledgedGroup, AcknowledgedPerson


class ListAcknowledgedGroups(APITestCase):
    def setUp(self):
        self.list_acknowledged_groups_url = '/acknowledgements/list-acknowledged-groups/'
        self.test_acknowledged_group = AcknowledgedGroup.objects.create(
            title='Photographers'
        )

    def test_listing_acknowledged_groups(self):
        response = self.client.get(self.list_acknowledged_groups_url, format='json')
        utils.print_response_info(response, test_name='List Acknowledged Groups Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class ListSelectAcknowledgedPeople(APITestCase):
    def setUp(self):
        self.list_acknowledged_people_url = '/acknowledgements/list-acknowledged-people/'
        self.select_acknowledged_person_url = '/acknowledgements/select-acknowledged-person/'
        self.test_acknowledged_group = AcknowledgedGroup.objects.create(
            title='Photographers'
        )
        self.test_acknowledged_person = AcknowledgedPerson.objects.create(
            first_name='Donal',
            last_name='Osullivan',
            group=self.test_acknowledged_group
        )

    def test_listing_acknowledged_people(self):
        response = self.client.get(self.list_acknowledged_people_url, format='json')
        utils.print_response_info(response, test_name='List Acknowledged People Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_selecting_acknowledged_person(self):
        data = {'acknowledged_person_id': self.test_acknowledged_person.id}
        response = self.client.post(self.select_acknowledged_person_url, data, format='json')
        utils.print_response_info(response, test_name='Select Acknowledged Person Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
