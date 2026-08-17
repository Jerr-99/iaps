FROM python:3.11-slim

# Set work directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postgresql-client \
    curl \
    git \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip
RUN pip install --upgrade pip setuptools wheel

# Copy requirements
COPY requirements.txt /app/

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy project
COPY . /app/

# Create necessary directories
RUN mkdir -p /app/logs /app/staticfiles /app/media

# Collect static files (if DEBUG=False)
RUN python manage.py collectstatic --noinput --clear || true

# Create a non-root user
RUN useradd -m -u 1000 django_user && chown -R django_user:django_user /app
USER django_user

# Expose port
EXPOSE 8000

# Run gunicorn
CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "4", "--timeout", "120"]
