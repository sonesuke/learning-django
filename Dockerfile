FROM amd64/python:3.9-buster

RUN apt -y update && apt -y install jq
ADD requirements.txt /requirements.txt
RUN pip install -r /requirements.txt