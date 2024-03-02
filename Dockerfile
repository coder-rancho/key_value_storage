# Use an official Python runtime as a parent image
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9

# Install supervisor
RUN apt-get update && apt-get install -y supervisor

# make them executable
# RUN chmod +x /usr/src/app/scripts/*.sh

# Set the working directory to /app
WORKDIR /app

# Copy only the requirements file to the container
COPY requirements.txt /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Copy supervisord configs and scripts
COPY supervisord.conf /etc/supervisord.conf

# Copy the current directory contents into the container at /app
COPY . /app

# Define environment variable for FastAPI to run in "production" mode
# ENV FASTAPI_ENV=development

# Run app.py when the container launches
CMD ["/usr/bin/supervisord"]