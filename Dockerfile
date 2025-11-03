# Use Python 3.12 slim image as base (stable version)
FROM python:3.12-slim-bookworm

# Set working directory
WORKDIR /app

# Install system dependencies and security updates
RUN apt-get update && apt-get install -y \
    ffmpeg \
    build-essential \
    gcc \
    && apt-get upgrade -y \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /tmp/* \
    && rm -rf /var/tmp/*

# Upgrade pip first
RUN pip install --no-cache-dir --upgrade pip

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY youtube_to_mp3.py .

# Create a non-root user for security
RUN adduser --disabled-password --gecos '' appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose the port FastAPI will run on
EXPOSE 8000

# Command to run the FastAPI application with uvicorn
CMD ["uvicorn", "youtube_to_mp3:app", "--host", "0.0.0.0", "--port", "8000"]