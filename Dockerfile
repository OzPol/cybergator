FROM python:3.12-slim

WORKDIR /app

# installation of only the necessary dependencies for linux
# this helps to keep the container lightweight
RUN apt-get update && apt-get install -y \
  curl \
  libpq-dev \
  postgresql-client \
  gcc \
  && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-interaction --no-root --no-cache
    
COPY . .

EXPOSE 8000

CMD ["poetry", "run", "python", "app.py"]