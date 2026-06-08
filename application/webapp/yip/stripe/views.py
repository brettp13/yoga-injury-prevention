from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response

from rabbit_tasks.tasks import add_user_to_stripe, remove_user_from_stripe
from campaign_tracker.models import MarketingCampaign
from user_profiles.models import UserProfile
from .models import Subscriber


class CreateSubscriber(APIView):
    def post(self, request):
        stripe_token = request.data['token']
        email = request.data['email']

        print(stripe_token, flush=True)

        user = self.request.user
        user_profile = UserProfile.objects.get(user=user)

        subscriber = Subscriber.objects.create(user_auth=user, user_profile=user_profile)
        subscriber.save()


        add_user_to_stripe(email, stripe_token, subscriber.id)

        return Response('{"received_token": "true"}', status=status.HTTP_200_OK)


class WebHookEvent(APIView):
    def post(self, request):
        print(request.data, flush=True)
        return Response(status=status.HTTP_200_OK)
        

def create_subscriber(token, email, user, user_profile, traffic_source):
    try:
        campaign = MarketingCampaign.objects.get(name=traffic_source)
    except:
        campaign = MarketingCampaign.objects.get(name='organic')

    subscriber = Subscriber.objects.create(user_auth=user, user_profile=user_profile, campaign=campaign)
    subscriber.save()

    add_user_to_stripe(email, token, subscriber.id)

