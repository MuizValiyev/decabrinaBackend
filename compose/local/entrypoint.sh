python manage.py migrate

python manage.py collectstatic --noinput

exec gunicorn decabrina.wsgi:application --bind 0.0.0.0:8000
