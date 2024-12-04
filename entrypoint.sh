#!/bin/sh

echo "Waiting for the database to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$DB_USER"; do
  echo "Waiting for PostgreSQL to be ready..."
  sleep 1
done
echo "Database is ready."

python3 manage.py makemigrations --noinput
python3 manage.py migrate

if [ "$DJANGO_SUPERUSER_USERNAME" ] && [ "$DJANGO_SUPERUSER_PASSWORD" ]; then
        if ! python3 manage.py shell -c "from django.contrib.auth import get_user_model; exit(0 if get_user_model().objects.filter(username='$DJANGO_SUPERUSER_USERNAME').exists() else 1)"; then
        echo "Creating superuser..."
        python3 manage.py createsuperuser --noinput
    else
        echo "Superuser already exists."
    fi
fi

python3 manage.py test api

if [ ! -f /usr/src/app/data/seeded ]; then
    python3 manage.py seed_standards
    touch /usr/src/app/data/seeded 
    echo "Seeded standards"
    else
    echo "Standards already seeded."
fi

if [ ! -f /usr/src/app/data/imported ]; then
    python3 manage.py import_pollution_data /usr/src/app/data/data.csv
    touch /usr/src/app/data/imported 
    echo "Imported pollution data"
    else
    echo "Pollution data already imported."
fi

exec "$@"