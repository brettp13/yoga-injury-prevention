import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from conditions.models import Condition
from testing_utils import utils
from user_profiles.models import SearchEntry
from yogaposes.models import BeneficialPoses, YogaPose


class SearchByConditionContraindicatedPoses(APITestCase):
    def setUp(self):
        self.url = '/search-by-conditions/get-contraindicated-poses/'
        self.test_condition = Condition.objects.create(name='corona virus')
        self.test_pose_1 = YogaPose.objects.create(
                english_name='Downward Dog')
        self.test_pose_1.contraindicated_conditions.add(self.test_condition)
        self.test_pose_2 = YogaPose.objects.create(
                english_name='Mountain Pose')
        self.test_pose_2.contraindicated_conditions.add(self.test_condition)
        self.test_user = utils.create_test_user()
        self.test_user_profile = utils.create_test_user_profile(user=self.test_user)
        self.token = Token.objects.get(user=self.test_user)

    def test_get_contraindicated_poses_for_one_condition(self):
        data = {'conditions': [self.test_condition.id,]}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.url, data, format='json')
        utils.print_response_info(response, test_name='Get Contraindicated Poses For One Condition Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchByConditionIndicatedPoses(APITestCase):
    def setUp(self):
        self.url = '/search-by-conditions/get-indicated-poses/'
        self.test_condition = Condition.objects.create(name='corona virus')
        self.test_condition_special_case = Condition.objects.create(
                name='Lower Back Pain', special_case=True)
        self.test_pose = YogaPose.objects.create(
            english_name='Downward Dog')
        self.test_pose_2 = YogaPose.objects.create(
            english_name='Warrior 1'
        )
        self.test_beneficial_mapper = BeneficialPoses.objects.create(
            condition=self.test_condition, why_these_poses_help='the blood flow to the brain helps kill corona')
        self.test_benefecial_mapper_2 = BeneficialPoses.objects.create(
            condition=self.test_condition_special_case, why_these_poses_help='Nothing helps this one. Bitch')
        self.test_beneficial_mapper.poses.add(self.test_pose)
        self.test_beneficial_mapper.poses.add(self.test_pose_2)
        self.test_user = utils.create_test_user()
        self.test_user_profile = utils.create_test_user_profile(user=self.test_user)
        self.token = Token.objects.get(user=self.test_user)

    def test_get_indicated_poses(self):
        data = {'conditions': [self.test_condition.id, self.test_condition_special_case.id]}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.url, data, format='json')
        utils.print_response_info(response, test_name='Get Indicated Poses Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)


class SearchByConditionSafePoses(APITestCase):
    def setUp(self):
        self.url = '/search-by-conditions/get-safe-poses/'
        self.test_condition = Condition.objects.create(name='corona virus')
        self.test_pose = YogaPose.objects.create(english_name='Downward Dog')
        self.test_pose_2 = YogaPose.objects.create(english_name='Warrior 1')
        self.test_pose.contraindicated_conditions.add(self.test_condition)
        self.test_user = utils.create_test_user()
        self.test_profile = utils.create_test_user_profile(user=self.test_user)
        self.token = Token.objects.get(user=self.test_user)

    def test_get_safe_poses(self):
        data = {'conditions': [self.test_condition.id]}
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        response = self.client.post(self.url, data, format='json')
        utils.print_response_info(response, test_name='Get Safe Poses Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
