# Use Python 3.10 slim image
FROM python:3.11-slim

# Set environment variable to disable interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Install dependencies
RUN apt-get update && apt-get install -y \
    git \
    && rm -rf /var/lib/apt/lists/*

# Set working directory in the container
WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Copy app code into the container
COPY . /app/

# Expose the port for the API (default 8000)
EXPOSE 8000

# Run the app
CMD ["python", "app/main.py"]
