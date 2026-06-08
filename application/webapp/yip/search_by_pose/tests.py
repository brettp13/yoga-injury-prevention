import json

from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from django.contrib.auth.models import User

from conditions.models import Condition, ConditionCategory
from testing_utils import utils
from user_profiles.models import SearchEntry
from yogaposes.models import YogaPose, BeneficialPoses


class SearchByPose(APITestCase):
    def setUp(self):
        self.search_by_pose_url = '/search-by-pose/search-by-pose/'
        self.test_pose = YogaPose.objects.create(english_name='Downward dog')
        self.test_pose.save()
        self.test_user = utils.create_test_user()
        self.test_user_profile = utils.create_test_user_profile(self.test_user)
        self.token = Token.objects.get(user=self.test_user)

    def test_seaching_by_pose(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {'yoga_pose_id': self.test_pose.id}
        response = self.client.post(self.search_by_pose_url, data, format='json')
        utils.print_response_info(response, test_name='Search By Pose Test')

        search_entry = SearchEntry.objects.get(profile=self.test_user_profile)
        print('Search entry profile: %s, Search entry criteria: %s' % (search_entry.profile, search_entry.search_criteria))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['english_name'], 'Downward dog')
        self.assertEqual(search_entry.search_criteria, self.test_pose.sanskrit_name)


class GetConditionsHelpedByPose(APITestCase):
    def setUp(self):
        self.get_conditions_helped_by_pose_url = '/search-by-pose/get-conditions-helped-by-pose/'
        self.test_pose = YogaPose.objects.create(english_name='Downward dog')
        self.test_pose.save()
        self.test_condition_category = ConditionCategory.objects.create(name='leg conditions')
        self.test_condition_category.save()
        self.test_condition = Condition.objects.create(
            name='tight hamstrings', category=self.test_condition_category)
        self.test_condition.save()
        self.beneficial_mapper = BeneficialPoses.objects.create(condition=self.test_condition)
        self.beneficial_mapper.poses.set([self.test_pose])
        self.beneficial_mapper.save()

        self.test_user = utils.create_test_user()
        self.test_user_profile = utils.create_test_user_profile(self.test_user)
        self.token = Token.objects.get(user=self.test_user)

    def test_get_conditions_helped_by_pose(self):
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + str(self.token))
        data = {'yoga_pose_id': self.test_pose.id}
        response = self.client.post(self.get_conditions_helped_by_pose_url, data, format='json')

        utils.print_response_info(response, test_name='Get Conditions Helped By Pose Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)[0]['name'], self.test_condition.name)
