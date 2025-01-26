# pull official base image
FROM python:3.13.1-slim-bookworm

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
#RUN apt-get install libpq-dev
#RUN apt-get install libpq5=12.12-0ubuntu0.20.04.1 && sudo apt-get install libpq-dev



RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN apt-get -y install netcat-traditional
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY staticfiles /home/app/web/staticfiles


# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["./entrypoint.sh"]