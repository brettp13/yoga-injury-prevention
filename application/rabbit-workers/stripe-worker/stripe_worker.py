import json
import os
import pika
import psycopg2
import stripe
import time


def connect_to_db():
    """
    Establish a connection to the database
    """
    db_connection_parameters = {
        'host': 'postgresql',
        'database': os.environ['DB_NAME'],
        'user': os.environ['DB_USER'],
        'password': os.environ['DB_PASSWORD']
    }

    try:
        connection = psycopg2.connect(**db_connection_parameters)
        return connection
    except Exception as e:
        print(e, flush=True)


def create_subscriber(email, token, subscriber_id):
    """
    Create a subscriber in stripe
    """
    try:
        print('TRYING TO CREATE CUSTOMER', flush=True)
        stripe_customer = stripe.Customer.create(
            email=email, source=token
        )

        # Log success
        customer_success = "CUSTOMER CREATED. ID: %s EMAIL: %s" % (stripe_customer.id, email)
        print(customer_success, flush=True)

        subscription = stripe.Subscription.create(
            customer=stripe_customer.id,
            items=[{
                'plan': 'plan_E1mutDCu2D5nIJ'
            }],
            trial_period_days=7
        )

        # Log subscription success
        subscription_success = "SUBSCRIBER CREATED. ID: %s" % subscription.id
        print(subscription_success, flush=True)

        # Update db subscription model
        query = """UPDATE stripe_subscriber
                   SET customer_id=%s WHERE id=%s"""

        connection = connect_to_db()
        cursor = connection.cursor()
        
        try:
            cursor.execute(query, (stripe_customer.id, subscriber_id))
            connection.commit()
            cursor.close()
        except Exception as e:
            connection.rollback()
            cursor.close()
            print(e, flush=True)
        connection.close()

    except Exception as e:
        print(e, flush=True)


def remove_subscriber(customer_id):
    """
    Remove subscriber from Stripe
    """
    try:
        print('REMOVING SUBSCRIBER FROM STRIPE', flush=True)
        stripe.Customer.delete(customer_id)

        print('CUSTOMER REMOVED', flush=True)


    except Exception as e:
        print(e, flush=True)


def stripe_actions(ch, method, properties, body):
    """
    Create subscriber in stripe
    """
    payload = json.loads(body.decode("utf-8"))
    action = payload['action_type']
    stripe.api_key = os.environ['PROD_STRIPE_SECRET']

    if action == 'add_user':
        email = payload['email']
        token = payload['stripe_token']
        subscriber_id = int(payload['subscriber_id'])
        create_subscriber(email, token, subscriber_id)
    elif action == 'remove_user':
        customer_id = payload['customer_id']
        remove_subscriber(customer_id)

    ch.basic_ack(delivery_tag = method.delivery_tag)


# Connect to rabbit
time.sleep(90)

try:
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host='rabbitmq'))
    channel = connection.channel()
except Exception as e:
    print(e, flush=True)

# Declare queue
try:
    channel.queue_declare(queue='stripe_actions', durable=True)
except Exception as e:
    print(e, flush=True)

# Start consuming
try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='stripe_actions', on_message_callback=stripe_actions)
    print(' [*] Waiting for stripe related tasks', flush=True)
    channel.start_consuming()
except Exception as e:
    print(e, flush=True)