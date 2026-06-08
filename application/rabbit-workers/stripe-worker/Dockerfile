FROM python:3.7

ADD requirements.txt /tmp/requirements.txt
RUN pip install -r /tmp/requirements.txt

RUN mkdir /stripe_actions
ADD stripe_worker.py /stripe_actions

WORKDIR /stripe_actions