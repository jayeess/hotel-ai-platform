# Backend Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install (backend subdirectory is build context)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Expose port
EXPOSE 8000

# Start command for Render: respect $PORT and set PYTHONPATH=.
CMD ["sh", "-c", "PYTHONPATH=. uvicorn main:app --host 0.0.0.0 --port $PORT"]

