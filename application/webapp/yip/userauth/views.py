from django.contrib.auth.models import User

from rest_framework import status, permissions
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from rabbit_tasks.tasks import add_to_mail_list, create_email, remove_user_from_stripe
from stripe.models import Subscriber
from user_profiles.models import UserProfile

from .serializers import UserAuthSerializer, AuthTokenViewSerializer


class CreateUserAuth(APIView):
    """
    Create a user auth object
    """
    def post(self, request):
        serializer = UserAuthSerializer(data=self.request.data, many=True)
        if serializer.is_valid():
            serializer.save()

            create_email(
                recipient=self.request.data[0]['email'],
                subject='Welcome to YIP',
                body='Thanks for signing up for a free trial!',
                email_type='free trial signup'
            )

            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserAuthDetail(APIView):
    """
    Select, edit or delete user auth objects.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        try:
            user = request.user
            serializer = UserAuthSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'Error': 'User does not exist'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        serializer = UserAuthSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        content = {'success': 'user deleted'}
        return Response(content, status=status.HTTP_200_OK)


class CustomAuthToken(APIView):
    """
    Override django-rest-framework default auth token view to use custom
    serializer. This way we can exclude the password hash from being exposed.
    """
    def post(self, request, *args, **kwargs):
        serializer = AuthTokenViewSerializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'id': user.pk, 'email': user.email})


class ForgotPassword(APIView):
    """
    Takes an email address, if an account is associated with that email address
        1. Reset the password
        2. Send the new password to the user
    """
    def post(self, request, *args, **kwargs):
        try:
            email = request.data['email'].lower()
            try:
                user = User.objects.get(email=email)

                if len(user.first_name) > 0:
                    new_password = "%s-likes-yoga" % user.first_name.lower()
                else:
                    new_password = "%s-likes-yoga" % email

                user.set_password(new_password)
                user.save()

                create_email(
                    recipient=email,
                    subject='YIP Password change',
                    body='Your new password: %s' % new_password,
                    email_type='forgot password'
                )

                content = {'status': 'success', 'message': 'Password reset'}
                http_status = status.HTTP_200_OK

            except Exception as e:
                content = {'status': 'error', 'message': 'No account associated with that address'}
                http_status = status.HTTP_400_BAD_REQUEST
        except Exception as e:
            content = {'status': 'error', 'message': 'Email address required'}
            http_status = status.HTTP_400_BAD_REQUEST

        return Response(content, http_status)


class CheckEmailAvailability(APIView):
    """
    Checks to see if the given email address is available, or already associated
    with another account.
    """
    def post(self, request, *args, **kwargs):
        email = request.data['email']
        
        try:
            user = User.objects.get(email=email)
            return Response(0, status=status.HTTP_200_OK)
        except:
            return Response(1, status=status.HTTP_200_OK)

class CheckPassword(APIView):
    """
    Checks to see if the given password is correct for the user associated
    with the request.
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)
    
    def post(self, request, *args, **kwargs):
        try:
            password = request.data['password']
            user = request.user
            if user.check_password(password):
                return Response(1, status=status.HTTP_200_OK)
            else:
                return Response(0, status=status.HTTP_200_OK)
        except Exception as e:
            print(e, flush=True)
            content = {'status': 'error', 
                       'message': 'missing password or invalid user'}
            return Response(content, status=status.HTTP_400_BAD_REQUEST)


class CancelAccount(APIView):
    """
    Delete user account
    """
    authentication_classes = (TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user
        profile = UserProfile.objects.get(user=user)

        # Send user an email confirming account cancellation
        create_email(
                recipient=request.user.email,
                subject='YIP Cancellation',
                body='This is a confirmation that your account with us has been cancelled. Thanks and best regards, YIP',
                email_type='account cancellation'
        )

        # Send us an email with the user info
        message = """
            User Info:
            First name: %s
            Last name: %s
            Email: %s
            Reason for cancellation: %s
            """ % (profile.first_name, 
                   profile.last_name, 
                   user.email, 
                   request.data['cancelReason'])

        create_email(
            recipient='info@yip.guru',
            subject='YIP Cancellation',
            body=message,
            email_type='account cancellation'
        )

        # Move user to ex-subscribers mail list on mailchimp
        add_to_mail_list(
            user.email, profile.first_name, profile.last_name, 'ex-subscribers')

        subscriber = Subscriber.objects.get(user_auth=user)

        # Remove user from stripe
        remove_user_from_stripe(subscriber.customer_id)

        # Delete user auth
        user.delete()
        
        content = {'success': 'user has been disabled'}
        return Response(content, status=status.HTTP_200_OK)
