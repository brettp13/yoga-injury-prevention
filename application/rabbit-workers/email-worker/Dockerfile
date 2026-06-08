FROM python:3.7

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /send_emails
ADD email_worker.py /send_emails

WORKDIR /send_emails
