from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import YogaPose, WorkAroundYogaPose
from .serializers import YogaPoseSerializer, WorkaroundSerializer


class ListSelectPoses(APIView):
    """
    List poses, or select a single one.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        List poses
        """
        yoga_poses = YogaPose.objects.all()
        serializer = YogaPoseSerializer(yoga_poses, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        """
        Select a single pose
        """
        try:
            yoga_pose_id = request.data['yoga_pose_id']
            yoga_pose = YogaPose.objects.get(id=yoga_pose_id)
            serializer = YogaPoseSerializer(yoga_pose)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'yoga_pose_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class Workarounds(APIView):
    """
    Get a workaround (if exists)
    """
    def post(self, request):
        try:
            # Make sure user sent a yogapose_id and condition_id with the request
            yogapose_id = request.data['yoga_pose_id']
            condition_id = request.data['condition_id']

            workaround = WorkAroundYogaPose.objects.filter(
                yogapose=yogapose_id, condition=condition_id)

            if workaround:
                serializer = WorkaroundSerializer(workaround)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response('', status=status.HTTP_200_OK)
        
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'yogapose_id and/or condition_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
