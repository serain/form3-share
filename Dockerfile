FROM python:3.7-buster

COPY form3 /app/form3
COPY tests /app/tests
COPY Pipfile Pipfile.lock /app/

WORKDIR /app/

RUN pip install pipenv==2018.11.26
RUN pipenv install --dev
