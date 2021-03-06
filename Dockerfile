FROM amd64/python:3.9-buster

RUN apt -y update && apt -y install jq
RUN pip install django psycopg2-binary