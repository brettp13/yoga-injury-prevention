import json

from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from conditions.models import Condition
from conditions.serializers import ConditionSerializer
from utils.utils import (
    get_contraindicated_poses, 
    get_indicated_poses, 
    get_beneficial_poses,
    get_safe_poses, 
    increment_searches, 
    get_conditions_searched)
from yogaposes.models import BeneficialPoses
from yogaposes.serializers import YogaPoseSerializer


class SearchForContraindicatedPoses(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            conditions_searched = request.data['conditions'] # gives us the array of condition ids passed in request.data
            searched_conditions = get_conditions_searched(conditions_searched)
            poses = get_contraindicated_poses(conditions_searched)

            condition_serializer = ConditionSerializer(searched_conditions, many=True)
            pose_serializer = YogaPoseSerializer(poses, many=True)

            data = {'search_type': 'contraindicated poses',
                    'conditions_searched': condition_serializer.data,
                    'contraindicated_poses': pose_serializer.data}

            increment_searches(
                user=request.user, conditions=conditions_searched, search_type='contraindicated')

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'conditions missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SearchForIndicatedPoses(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            conditions_searched = request.data['conditions']
            yoga_poses_and_conditions, searched_conditions = get_indicated_poses(conditions_searched)

            data = {'search_type': 'beneficial poses',
                    'yogaposes_and_beneficial_conditions': yoga_poses_and_conditions,
                    'conditions_searched': searched_conditions}

            increment_searches(
                user=request.user, conditions=conditions_searched, search_type='indicated')

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'conditions missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class SearchForBeneficialPoses(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            condition_ids = request.data['conditions']
            beneficial_poses, conditions_searched = get_beneficial_poses(condition_ids)

            data = {'search_type': 'beneficial_poses',
                    'beneficial_poses': beneficial_poses,
                    'conditions_searched': conditions_searched}

            increment_searches(
                user=request.user, conditions=condition_ids, search_type='beneficial'
            )

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'conditions missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class WhyYogaHelps(APIView):
    """
    Returns yogaposes.models.BeneficialPoses.why_these_poses_help for the condition
    passed.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            condition_id = request.data['condition_id']
            condition = Condition.objects.get(id=condition_id)
            beneficial_pose = BeneficialPoses.objects.get(condition=condition)
            data = {'how_yoga_helps': beneficial_pose.why_these_poses_help}
            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'conditions missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class SearchForSafePoses(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        yoga_poses = []
        conditions = []
        try:
            conditions_searched = request.data['conditions']
            safe_poses, searched_conditions = get_safe_poses(conditions_searched)

            for condition in searched_conditions:
                serializer = ConditionSerializer(condition)
                conditions.append(serializer.data)

            for pose in safe_poses:
                serializer = YogaPoseSerializer(pose)
                yoga_poses.append(serializer.data)

            data = {'search_type': 'safe poses',
                    'conditions_searched': conditions,
                    'safe_poses': yoga_poses}

            increment_searches(
                user=request.user,
                conditions=conditions_searched,
                search_type='safe'
            )

            return Response(data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'conditions missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
