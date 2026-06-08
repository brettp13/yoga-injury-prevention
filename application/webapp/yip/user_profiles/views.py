from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.views import APIView

from rabbit_tasks.tasks import create_email, add_to_mail_list
from stripe.views import create_subscriber
from .models import UserProfile, YogaStyle
from .serializers import UserProfileSerializer, YogaStyleSerializer, SearchEntrySerializer


class CreateUserProfile(APIView):
    """
    Create a user profile
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        yoga_style_id = request.data['yoga_style']
        try:
            yoga_style = YogaStyle.objects.get(id=yoga_style_id)
        except:
            yoga_style = YogaStyle.objects.get(title='unknown')

        # Find traffic source
        traffic_source = request.data['traffic_source']

        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, yoga_style=yoga_style)

            first_name = request.data['first_name']
            last_name = request.data['last_name']
            email = request.user.email

            user_profile = UserProfile.objects.get(user=request.user)

            # Create subscriber
            create_subscriber(request.data['token'], 
                              email, 
                              request.user, 
                              user_profile, 
                              traffic_source)

            email_body = '''
                         New subscriber info:
                         first name: %s
                         last name: %s
                         email: %s
                         yoga style: %s
                         ''' % (first_name, last_name, email, yoga_style)

            # Add user to mailchimp
            add_to_mail_list(
                email=email,
                fname=first_name,
                lname=last_name,
                list_name='subscribers'
            )

            # Send email to info@yip.guru about a new conversion
            create_email(
                recipient='info@yip.guru',
                subject='New subscriber',
                body=email_body,
                email_type='new subscriber'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileDetail(APIView):
    """
    Edit, delete or select a user profile
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data)

        # Check for yoga_style
        try:
            yoga_style_id = request.data['yoga_style']
            yoga_style = YogaStyle.objects.get(id=yoga_style_id)
        except:
            yoga_style = None

        if serializer.is_valid():
            if yoga_style:
                serializer.save(yoga_style=yoga_style)
            else:
                serializer.save()

            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        profile = UserProfile.objects.get(user=request.user)

        # Move user to mailchimp ex-subscribers list
        add_to_mail_list(
            email=request.user.email,
            fname=profile.first_name,
            lname=profile.last_name,
            list_name='ex-subscribers'
        )

        profile.delete()
        content = {'success': 'profile deleted'}
        return Response(content, status=status.HTTP_200_OK)

    def post(self, request):
        # Select and return user profile
        try:
            profile = UserProfile.objects.get(user=request.user)
            serializer = UserProfileSerializer(profile)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            message = {'error': 'user profile does not exist'}
            return Response(message, status=status.HTTP_400_BAD_REQUEST)


class ListCreateYogaStyles(APIView):
    """
    Create a Yoga style
    """
    def post(self, request):
        serializer = YogaStyleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        yoga_styles = YogaStyle.objects.filter(public=True)
        serializer = YogaStyleSerializer(yoga_styles, many=True)
        return Response(serializer.data, status.HTTP_200_OK)


class CreateSearchEntry(APIView):
    """
    Create a search entry
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = SearchEntrySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(profile=profile)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
