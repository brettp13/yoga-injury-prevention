import json
import os
import pika
import smtplib
import time

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def send_email(ch, method, properties, body):
    """
    Send email from application.
    """
    payload = json.loads(body.decode("utf-8"))

    email_type = payload['email_type']
    sender = os.environ['EMAIL_HOST_USER']
    recipient = payload['recipient']
    subject = payload['subject']
    body = payload['body']

    message = MIMEMultipart()
    message['From'] = sender
    message['To'] = recipient
    message['Subject'] = subject

    body = MIMEText(body, 'plain')

    message.attach(body)

    try:
        server = smtplib.SMTP_SSL(os.environ['EMAIL_HOST'], os.environ['EMAIL_HOST_PORT'])
        server.ehlo()
        server.login(sender, os.environ['EMAIL_HOST_PASSWORD'])
        server.sendmail(sender, recipient, message.as_string())
        server.close()

        print('Sent %s email' % email_type, flush=True)
    except Exception as e:
        print('Something broke', flush=True)
        print(e, flush=True)

    # ack message
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
    channel.queue_declare(queue='emails_to_send', durable=True)
except Exception as e:
    print(e, flush=True)

# Start consuming
try:
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue='emails_to_send', on_message_callback=send_email)
    print(' [*] Waiting for email to send', flush=True)
    channel.start_consuming()
except Exception as e:
    print(e, flush=True)
