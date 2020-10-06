FROM python:3.6-slim

VOLUME /data
WORKDIR /code
COPY Pipfile *.py scripts/start_service.sh ./
RUN pip install pipenv
RUN pipenv install --three


# command to run on container start
CMD [ "bash", "start_service.sh" ]
