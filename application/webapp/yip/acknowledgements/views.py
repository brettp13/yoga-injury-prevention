from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AcknowledgedGroup, AcknowledgedPerson
from .serializers import AcknowledgedGroupSerializer, AcknowledgedPersonSerializer


class ListAcknowledgedGroups(APIView):
    def get(self, request):
        acknowledged_groups = AcknowledgedGroup.objects.all()
        serializer = AcknowledgedGroupSerializer(acknowledged_groups, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ListSelectAcknowledgedPerson(APIView):
    def get(self, request):
        acknowledged_people = AcknowledgedPerson.objects.all()
        serializer = AcknowledgedPersonSerializer(acknowledged_people, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            acknowledged_person_id = request.data['acknowledged_person_id']
            acknowledged_person = AcknowledgedPerson.objects.get(id=acknowledged_person_id)
            serializer = AcknowledgedPersonSerializer(acknowledged_person)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'acknowledged_person_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
