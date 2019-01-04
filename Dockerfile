FROM python:alpine

MAINTAINER Menangen <menangen@gmail.com>

WORKDIR /opt/app/

# COPY requirements.txt /opt/app/
# RUN pip install --no-cache-dir -r requirements.txt

RUN pip install --no-cache-dir docker

COPY *.py /opt/app/

VOLUME /var/run/docker.sock:/var/run/docker.sock

CMD [ "python", "/opt/app/manage.py" ]