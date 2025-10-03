FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install build deps and cleanup to keep image small
RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy app
COPY . /app

EXPOSE 3010

# Use a non-root user in production ideally; using root here for simplicity
CMD ["python", "main.py"]
