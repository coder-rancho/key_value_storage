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

# Define an entrypoint script
ENTRYPOINT ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]

# Additional commands can be specified in CMD
CMD ["huey_consumer.py", "app.huey_tasks.huey"]