uv run python manage.py makemigrations --noinput
uv run python manage.py migrate --noinput
uv run python manage.py collectstatic --noinput

uv run uvicorn psyeco_backend.asgi:application --host 0.0.0.0 --port 8008 --reload --proxy-headers --forwarded-allow-ips="*"