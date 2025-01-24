# Use Ubuntu as the base image
FROM ubuntu:latest

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV VIRTUAL_ENV=/opt/venv

# Install dependencies
RUN apt update && apt install -y \
    python3-pip \
    python3-venv \
    python3-dev \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Create a virtual environment
RUN python3 -m venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Set the working directory
WORKDIR /app

# Copy the application requirements
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Django application
COPY . /app/

# Expose the application port
EXPOSE 8000

# Run the Gunicorn server
CMD ["gunicorn", "myproject.wsgi:application", "--bind", "0.0.0.0:8000"]
