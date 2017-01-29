FROM python:3.5

ADD . /project
WORKDIR /project

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN chmod +x /project/bin/uwsgi.sh
