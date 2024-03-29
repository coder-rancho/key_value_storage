# Use an official Python runtime as a parent image
FROM python:3.10

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable for FastAPI to run in "production" mode

# ENV FASTAPI_ENV=development

# Set REDIS_SERVICE_NAME based on deployment context:
# - Docker Compose: service name from docker-compose.yml
# - Kubernetes: metadata.name from redis-service.yml
# - Cloud Redis: IP address or hostname of the server
ENV REDIS_SERVICE_NAME='redis'

# Run app.py when the container launches
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
