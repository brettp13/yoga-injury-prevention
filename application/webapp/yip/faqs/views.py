from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import FAQ
from .serializers import FAQSerializer


class ListSelectFAQs(APIView):
    """
    List FAQs or select a single FAQ
    """
    def get(self, request):
        """
        List FAQs
        """
        faqs = FAQ.objects.all()
        serializer = FAQSerializer(faqs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            faq_id = request.data['faq_id']
            faq = FAQ.objects.get(id=faq_id)
            serializer = FAQSerializer(faq)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'faq_id missing or invalid'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)
