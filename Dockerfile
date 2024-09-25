# Use Python 3.12 base image
FROM python:3.12-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy cache warmer script
COPY cache_warmer/cache_warmer.py .

# Copy csv file
COPY cache_warmer/csv/urls.csv csv/

# Copy cert file
COPY /cert/ca_cert.pem cert/

# Run cache warmer script
CMD ["python", "cache_warmer.py"]