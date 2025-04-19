FROM python:3.10-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Set environment variables
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

# Check Python and pip installations
RUN python --version && pip --version

# Create a wrapper script to handle environment variables
RUN echo '#!/bin/bash\n\
port=${PORT:-8080}\n\
echo "Starting server on port $port"\n\
exec uvicorn main:app --host 0.0.0.0 --port $port --log-level debug\n\
' > /app/start.sh && chmod +x /app/start.sh

# Run with wrapper script
CMD ["/app/start.sh"] 