# Use official slim Python base image for smaller attack surface
FROM python:3.12-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Create a non-root user
RUN addgroup --system django && adduser --system --group --no-create-home django

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libsqlite3-0 gcc \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Change ownership to non-root user
RUN chown -R django:django /app

# Switch to non-root user
USER django

# Expose port (optional if behind reverse proxy)
EXPOSE 8000

# Collect static files (if needed)
RUN python manage.py collectstatic --noinput

# Default command
CMD ["gunicorn", "your_project_name.wsgi:application", "--bind", "0.0.0.0:8000"]
