from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from utils.utils import increment_searches
from conditions.models import Condition
from conditions.serializers import ConditionSerializer
from yogaposes.models import YogaPose, BeneficialPoses
from yogaposes.serializers import YogaPoseSerializer


class SearchByPose(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        try:
            yoga_pose_id = request.data['yoga_pose_id']
            yoga_pose = YogaPose.objects.get(id=yoga_pose_id)
            serializer = YogaPoseSerializer(yoga_pose)

            increment_searches(user=request.user, yogapose=yoga_pose)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'yoga_pose_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

class GetConditionsHelpedByPose(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        conditions_helped_by_pose = []
        try:
            yoga_pose_id = request.data['yoga_pose_id']
            yoga_pose = YogaPose.objects.get(id=yoga_pose_id)
            beneficial_mappers = BeneficialPoses.objects.filter(
                poses__id__in=[yoga_pose.id]).distinct()

            for beneficial_mapper in beneficial_mappers:
                condition = beneficial_mapper.condition
                conditions_helped_by_pose.append(condition)
            
            serializer = ConditionSerializer(conditions_helped_by_pose, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'yoga_pose_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class GetConditionsContraindicatedByPose(APIView):
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        conditions_contraindicated_by_pose = []
        try:
            yoga_pose_id = request.data['yoga_pose_id']
            yoga_pose = YogaPose.objects.get(id=yoga_pose_id)
            
            contraindicated_conditions = yoga_pose.contraindicated_conditions.all()
            
            for condition in contraindicated_conditions:
                conditions_contraindicated_by_pose.append(condition)

            serializer = ConditionSerializer(conditions_contraindicated_by_pose, many=True)

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'yoga_pose_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)