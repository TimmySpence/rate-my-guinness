# Use a lightweight Python base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/* \
    && pip install --no-cache-dir -r requirements.txt


# Copy application code
COPY . .
COPY docker/wait-for-postgres.sh /app/wait-for-postgres.sh
RUN chmod +x /app/wait-for-postgres.sh

# Set environment variables (can be overridden in deployment)
ENV FLASK_ENV=production

# Set the google maps API key
# This can be set at build time using --build-arg GOOGLE_MAPS_API_KEY=your_key
ARG GOOGLE_MAPS_API_KEY
ENV GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}

# Expose the port Flask or Gunicorn will listen on
EXPOSE 5000

# Run with Gunicorn (adjust module name if needed, e.g. app:app)
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
