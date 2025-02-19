# scarico un immagine slim di Python 3.13
FROM python:3.13.1-slim-bookworm

#Imposto la directory in cui voglio lavorare localmente
WORKDIR /usr/src/app

# Imposto un approccio ottimizzato nello scrivere file temporanei di python come i files .pyc
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

#Configuro la distro. la slim-bookworm è su base debian, si gioca in casa
RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN apt-get update \
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2
RUN apt-get -y install netcat-traditional
RUN pip install -r requirements.txt

#Copio il file di entrypoint, è qui dove faccio fare i lavori iniziali di setup e partenza
COPY ./entrypoint.sh .

RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh

RUN chmod +x /usr/src/app/entrypoint.sh

COPY staticfiles /home/app/web/staticfiles
COPY /docs/apidocs /home/app/web/staticfiles


# Copio il progetto. Può essere ottimizzato escludendo dei sub folder. Lo segno come TODO.
COPY . .

# eseguo l'entripoint e lo definisco come tale
ENTRYPOINT ["./entrypoint.sh"]