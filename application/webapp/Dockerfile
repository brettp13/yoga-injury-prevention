FROM python:3.7

ADD yip /opt/yip
ADD bin /opt/bin

RUN pip install -r /opt/yip/requirements.txt
RUN [ "chmod", "+x", "/opt/bin/build.sh" ]

WORKDIR /opt/yip
