# Use an official Python 3.10.12 slim image as a base
FROM python:3.10.12-slim as builder

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels gunicorn

# Final Stage
FROM python:3.10.12-slim

# Create a non-privileged user to run the app
RUN groupadd -r appgroup && useradd -r -g appgroup -s /sbin/nologin appuser

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PATH="/home/appuser/.local/bin:${PATH}"

# Set the working directory
WORKDIR /app

# Copy wheels from builder and install
COPY --from=builder /app/wheels /wheels
COPY --from=builder /app/requirements.txt .
RUN pip install --no-cache-dir /wheels/*

# Copy the project files
COPY --chown=appuser:appgroup . .

# Ensure necessary directories exist and have correct permissions
RUN mkdir -p /app/static /app/media && \
    chown -R appuser:appgroup /app/static /app/media /app

# Ensure the database file has correct permissions
# SQLite needs the directory to be writable for lock files
RUN if [ -f db.sqlite3 ]; then chown appuser:appgroup db.sqlite3 && chmod 664 db.sqlite3; fi

# Switch to the non-privileged user
USER appuser

# Expose the application port
EXPOSE 8000

# High-security production-ready command
# Using gunicorn for better security and performance than manage.py runserver
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "--access-logformat", "%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\"", "ems.wsgi:application"]
