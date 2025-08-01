FROM mcr.microsoft.com/devcontainers/python:0-3.10

# Install PostgreSQL client
RUN apt-get update && apt-get install -y postgresql-client

# Set the working directory
WORKDIR /workspace

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt