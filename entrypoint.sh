#!/bin/sh

echo "Waiting for postgres..."

while ! nc -z $SQL_HOST $SQL_PORT; do
    sleep 0.1
done
echo "PostgreSQL started"

python manage.py flush --no-input
python manage.py migrate
python manage.py createsuperuser --noinput --username=admin


CONTAINER_ALREADY_STARTED="FLAG_SET_ex"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    python manage.py shell < initBookingEntities.py
else
    echo "-- Not first container startup --"
fi



exec "$@"
