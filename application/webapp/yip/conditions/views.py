from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Condition, ConditionCategory
from .serializers import ConditionSerializer, ConditionCategorySerializer


class ListSelectConditions(APIView):
    """
    List conditions, or select a single one.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        List conditions.
        """
        conditions = Condition.objects.all()
        serializer = ConditionSerializer(conditions, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        """
        Select a single condition.
        """
        try:
            condition_id = request.data['condition_id']
            condition = Condition.objects.get(id=condition_id)
            serializer = ConditionSerializer(condition)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'condition_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class ListSelectConditionCategory(APIView):
    """
    List condition categories or select a category.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        """
        List condition categories.
        """
        condition_categories = ConditionCategory.objects.all()
        serializer = ConditionCategorySerializer(condition_categories, many=True)
        return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request):
        """
        Select a single condition category.
        """
        try:
            condition_category_id = request.data['condition_category_id']
            condition_category = ConditionCategory.objects.get(id=condition_category_id)
            serializer = ConditionCategorySerializer(condition_category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'condition_category_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
