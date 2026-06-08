import json
import pika

from utils.utils import create_email_wrapper, add_to_mail_list_wrapper


@create_email_wrapper
def create_email(recipient, subject, body, email_type):
    """
    Add an email to the emails_to_send_queue
    """
    email = {
                'recipient': recipient,
                'subject': subject,
                'body': body,
                'email_type': email_type
            }

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )

    channel = connection.channel()
    channel.queue_declare(queue='emails_to_send', durable=True)

    channel.basic_publish(
       exchange='',
       routing_key='emails_to_send',
       body=json.dumps(email),
       properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

@add_to_mail_list_wrapper
def add_to_mail_list(email, fname, lname, list_name):
    """
    Add a user to a given email list
    """
    user_info = {
                    'email': email,
                    'fname': fname,
                    'lname': lname,
                    'list_name': list_name
                }

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )

    channel = connection.channel()
    channel.queue_declare(queue='mailchimp_actions', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='mailchimp_actions',
        body=json.dumps(user_info),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

def add_user_to_stripe(email, stripe_token, subscriber_id):
    """
    Add a user to stripe
    """
    payload = {
        'email': email,
        'stripe_token': stripe_token,
        'subscriber_id': subscriber_id,
        'customer_id': 'NA',
        'action_type': 'add_user'
    }

    print(payload, flush=True)

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )

    channel = connection.channel()
    channel.queue_declare(queue='stripe_actions', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='stripe_actions',
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()

def remove_user_from_stripe(customer_id):
    """
    Remove user from stripe
    """
    payload = {
        'customer_id': customer_id,
        'action_type': 'remove_user'
    }

    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq')
    )

    channel = connection.channel()
    channel.queue_declare(queue='stripe_actions', durable=True)

    channel.basic_publish(
        exchange='',
        routing_key='stripe_actions',
        body=json.dumps(payload),
        properties=pika.BasicProperties(delivery_mode=2)
    )

    connection.close()