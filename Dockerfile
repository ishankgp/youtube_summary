FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Create start script
RUN echo '#!/bin/sh\nport=${PORT:-8080}\nexec python -m uvicorn main:app --host 0.0.0.0 --port $port --log-level info' > /app/start.sh && \
    chmod +x /app/start.sh

EXPOSE 8080

HEALTHCHECK --interval=5s --timeout=5s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:${PORT:-8080}/ || exit 1

# Run the application
CMD ["/app/start.sh"] 