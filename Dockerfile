# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Build stage: compile and install Python dependencies into a virtualenv.
# Compilers and headers stay in this stage and never reach the final image.
# ---------------------------------------------------------------------------
FROM python:3.14-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install the locked dependencies. requirements.txt is generated from
# pyproject.toml by uv (see the command at the top of that file) and pins every
# package with hashes, so --no-deps installs exactly what was resolved there.
# Copying it on its own means this layer is reused until dependencies change.
COPY requirements.txt /tmp/requirements.txt
RUN pip install --no-deps --require-hashes --requirement /tmp/requirements.txt

# ---------------------------------------------------------------------------
# Runtime stage: slim image with the virtualenv and the project source.
# ---------------------------------------------------------------------------
FROM python:3.14-slim

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
# 3. Use the virtualenv built in the previous stage.
# 4. Use production settings for everything run in the image, including the
#    Procfile's release (migrate) and web processes. manage.py defaults to the
#    local dev settings otherwise.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH" \
    DJANGO_SETTINGS_MODULE=dawnwagesinfo.settings.deploy

# Runtime library needed by psycopg2.
RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    libpq5 \
 && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv

# Use /app folder as a directory where the source code is stored.
WORKDIR /app

# Set this directory to be owned by the "wagtail" user, so that collectstatic
# can write to it below.
RUN chown wagtail:wagtail /app

# Copy the source code of the project into the container.
COPY --chown=wagtail:wagtail . .

# Use user "wagtail" to run the build commands below and the server itself.
USER wagtail

# Collect static files.
RUN python manage.py collectstatic --noinput --clear

# Start the application server. Database migrations are not run here: on
# Cabotage they run in the "release" process defined in the Procfile. When
# running locally, run them yourself with:
#   docker run --rm <image> python manage.py migrate
CMD gunicorn dawnwagesinfo.wsgi:application --bind 0.0.0.0:$PORT
