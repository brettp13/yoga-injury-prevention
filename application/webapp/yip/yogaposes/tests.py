import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from testing_utils import utils

from .models import YogaPose


class ListSelectPoses(APITestCase):
    def setUp(self):
        self.list_poses_url = '/yoga-poses/list-poses/'
        self.select_pose_url = '/yoga-poses/select-pose/'

        self.yoga_pose_1 = YogaPose.objects.create(
                english_name='English Name', sanskrit_name='Sanskrit Name')
        self.yoga_pose_2 = YogaPose.objects.create(
                english_name='English Name Two', sanskrit_name='Sanskrit Name Two')
        self.test_user = utils.create_test_user()
        self.token = Token.objects.get(user=self.test_user)

    def test_list_poses(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.get(self.list_poses_url, format='json')
        utils.print_response_info(response, test_name='List Yoga Poses Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_select_pose(self):
        data = {'yoga_pose_id': self.yoga_pose_1.id}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.select_pose_url, data, format='json')
        utils.print_response_info(response, test_name='Select Yoga Pose Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['english_name'], 'English Name')

