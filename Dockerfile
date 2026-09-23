# syntax=docker/dockerfile:1

# ---------------------------------------------------------------------------
# Build stage: compile and install Python dependencies into a virtualenv.
# Compilers and headers stay in this stage and never reach the final image.
# ---------------------------------------------------------------------------
FROM python:3.13-slim AS builder

ENV PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

RUN apt-get update --yes --quiet && apt-get install --yes --quiet --no-install-recommends \
    build-essential \
    libpq-dev \
 && rm -rf /var/lib/apt/lists/*

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install only the dependencies listed in pyproject.toml. Copying this file on
# its own means the layer is reused until the dependencies change, rather than
# on every source code change.
COPY pyproject.toml /tmp/pyproject.toml
RUN python -c "import tomllib; print('\n'.join(tomllib.load(open('/tmp/pyproject.toml', 'rb'))['project']['dependencies']))" > /tmp/requirements.txt \
 && pip install --requirement /tmp/requirements.txt

# ---------------------------------------------------------------------------
# Runtime stage: slim image with the virtualenv and the project source.
# ---------------------------------------------------------------------------
FROM python:3.13-slim

# Add user that will be used in the container.
RUN useradd wagtail

# Port used by this container to serve HTTP.
EXPOSE 8000

# Set environment variables.
# 1. Force Python stdout and stderr streams to be unbuffered.
# 2. Set PORT variable that is used by Gunicorn. This should match "EXPOSE"
#    command.
# 3. Use the virtualenv built in the previous stage.
ENV PYTHONUNBUFFERED=1 \
    PORT=8000 \
    PATH="/opt/venv/bin:$PATH"

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
