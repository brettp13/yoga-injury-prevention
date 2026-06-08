import json

from rest_framework import status
from rest_framework.test import APITestCase

from testing_utils import utils

from .models import FAQ


class ListSelectFAQs(APITestCase):
    def setUp(self):
        self.list_faqs_url = '/faqs/list-faqs/'
        self.select_faq_url = '/faqs/select-faq/'

        self.test_faq = FAQ.objects.create(
            question='What is a FAQ?', answer='A Frequently Asked Question')

    def test_listing_faqs(self):
        response = self.client.get(self.list_faqs_url, format='json')
        utils.print_response_info(response, test_name='List FAQs Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_select_faq(self):
        data = {'faq_id': self.test_faq.id}
        response = self.client.post(self.select_faq_url, data, format='json')
        utils.print_response_info(response, test_name='Select FAQ Test')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json.loads(response.content)['question'], 'What is a FAQ?')
