FROM python:3.13-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir pipenv

COPY Pipfile Pipfile.lock /app/

RUN pipenv install --system --deploy

COPY . /app/

EXPOSE 8000 8001

CMD ["sh", "-c", "python manage.py migrate && python manage.py runserver 0.0.0.0:8000 & daphne -b 0.0.0.0 -p 8001 core.asgi:application"]