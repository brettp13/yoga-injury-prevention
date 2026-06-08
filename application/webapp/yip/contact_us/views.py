from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import ContactMessage
from .serializers import ContactMessageSerializer

from rabbit_tasks.tasks import create_email


class CreateContactMessage(APIView):
    """
    Create a new contact message
    """
    def post(self, request):
        """
        Serialize and store contact message in the db
        """
        serializer = ContactMessageSerializer(data=request.data, many=True)
        if serializer.is_valid():
            serializer.save()

            message_body = """
            From: {name} \n
            Sender email address: {email} \n
            Message: {message}
            """.format(
                  name=serializer.data[0]['full_name'],
                  email=serializer.data[0]['email'],
                  message=serializer.data[0]['message']
                )

            create_email(
                recipient='info@yip.guru',
                subject='New contact us message',
                body=message_body,
                email_type='contact form'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)