FROM python:3.7

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /mailchimp
ADD mailchimp_worker.py /mailchimp/mailchimp_worker.py

WORKDIR /mailchimp
