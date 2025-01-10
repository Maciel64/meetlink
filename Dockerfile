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

WORKDIR /app/core/

RUN python manage.py migrate

EXPOSE 8000

CMD [ "bash", "-c", "python manage.py runserver 0.0.0.0:8000 & daphne -p 8001 -b 0.0.0.0 core.asgi:application" ]