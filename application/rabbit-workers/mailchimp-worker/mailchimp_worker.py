import json
import os
import pika
import time
from mailchimp3 import MailChimp


class YIPMailChimp:
    """
    Mailchimp functions
    """
    mailchimp_list_ids = {
        'subscribers': os.environ['MAILCHIMP_SUBSCRIBERS_ID'],
        'ex-subscribers': os.environ['EX_MAILCHIMP_SUBSCRIBERS_ID']
    }

    client = MailChimp(mc_api = os.environ['MAILCHIMP_API_KEY'],
                       mc_user = os.environ['MAILCHIMP_API_USER'], timeout=100)

    def get_list(self, list_name):
        """
        Return the members of a given list
        """
        client = self.client
        list_id = self.mailchimp_list_ids[list_name]
        return client.lists.members.all(list_id=list_id, get_all=True)

    def check_list_for_user(self, email, list_name):
        """
        Check to see if a user is on a given list
        """
        mail_list = self.get_list(list_name)
        member_id = None
        for member in mail_list['members']:
            if member['email_address'] == email:
                member_id = member['id']
        return member_id

    def remove_from_list(self, email, list_name):
        """
        Remove a user from a given list
        """
        client = self.client
        list_id = self.mailchimp_list_ids[list_name]
        user_id = self.check_list_for_user(email, list_name)

        if user_id:
            client.lists.members.delete(list_id=list_id, subscriber_hash=user_id)
        else:
            print('User does not exist', flush=True)



    def add_to_list(self, list_name, email, fname, lname):
        """
        Removes user from existing lists and adds user to the given list
        """
        client = self.client
        list_id = self.mailchimp_list_ids[list_name]

        self.remove_from_list(email, 'subscribers')
        self.remove_from_list(email, 'ex-subscribers')

        try:
            client.lists.members.create(
                    list_id, {
                                 'email_address': email,
                                 'status': 'subscribed',
                                 'merge_fields': {
                                     'FNAME': fname,
                                     'LNAME': lname
                                 }
                             })
        except Exception as e:
            print(e, flush=True)


def mailchimp(ch, method, properties, body):
    """
    Perform mailchimp task
    """
    payload = json.loads(body.decode("utf-8"))

    email = payload['email']
    fname = payload['fname']
    lname = payload['lname']
    list_name = payload['list_name']

    mc = YIPMailChimp()
    mc.add_to_list(list_name, email, fname, lname)

    # Ack message
    ch.basic_ack(delivery_tag = method.delivery_tag)


# Connect to rabbit
time.sleep(90)

try:
    connection = pika.BlockingConnection(
            pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
except Exception as e:
    print('Mailchimp function first try', flush=True)
    print(e, flush=True)

# Declare queue
try:
    channel.queue_declare(queue='mailchimp_actions', durable=True)
except Exception as e:
    print('Mailchimp function second try', flush=True)
    print(e, flush=True)

# Start consuming
try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='mailchimp_actions', on_message_callback=mailchimp)
    print(' [*] Waiting for mailchimp actions', flush=True)
    channel.start_consuming()
except Exception as e:
    print(e, flush=True)
