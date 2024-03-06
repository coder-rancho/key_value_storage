# Key-Value Storage App

This repository contains the source code and configurations for a key-value storage application built with FastAPI, Redis, and Huey.

# Demo
[![Loom Video Preview](https://i.ibb.co/g9ngvBZ/Screenshot-from-2024-03-06-18-05-31.png)](INSERT_VIDEO_LINK)

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
  - [Docker Compose](#docker-compose)
  - [Kubernetes](#kubernetes)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Accessing the Application](#accessing-the-application)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The Key-Value Storage App is a simple application that allows storing and retrieving key-value pairs. It utilizes FastAPI as the web framework, Redis as the data store, and Huey for background task processing.

## Prerequisites

Make sure you have the following tools installed:

- Docker (if using Docker Compose)
- kubectl and a Kubernetes cluster like minikube (if deploying to Kubernetes)

## Getting Started

### Docker Compose

1. Clone this repository:

    ```bash
    git clone <repository-url>
    cd key-value-storage-app
    ```

2. Build and run the Docker containers:

    ```bash
    docker-compose up --build
    ```

3. Access the FastAPI application at [http://localhost:8000](http://localhost:8000).

### Kubernetes

1. Apply the Kubernetes configurations:

    ```bash
    kubectl apply -f kubernetes/
    ```

2. Access the FastAPI application using the NodePort service. Get the NodePort:

    ```bash
    minikube service fastapi-service
    ```

    minikube will create a tunnel to your application and open in browser.

## Configuration

Adjust the application configuration in the following files:

- `config.py`: Configure environment variables.
- `docker-compose.yml`: Docker Compose configuration.
- `kubernetes/`: Kubernetes deployment and service configurations.

## API Endpoints

The following API endpoints are available:

### **1. GET /:**
- **Description:** Ping the server.
- **Request Type:** GET
- **Response:**
  ```json
  {"res": "Hello world"}
  ```

### **2. GET /get/{key}:**
- **Description:** Retrieve a value for a given key
- **Request Type:** GET
- **Url parameters:**
    - `{key}`:(string) The key for the value to retrieve.
- **Response:**
  ```json
  {"key": "example_key", "value": "example_value"}
  ```

### **3. PUT /put:**
- **Description:** Create a key-value pair.
- **Request Type:** PUT
- **Request Payload Format:**
    ```json
    {
     "key": "example_key",
     "value": "example_value"
    }
    ```
- **Response:**
  ```json
  {"message": "Key creation task enqueued", "task_id": "example_task_id"}
  ```

### **4. DELETE /delete/{key}:**
- **Description:** Delete a key-value pair
- **Request Type:** DELETE
- **Url parameters:**
    - `{key}`:(string) The key for the value to delete.
- **Response:**
  ```json
  {"message": "Key deletion task enqueued", "task_id": "example_task_id"}
  ```

### **2. GET /task-state-info/{id}:**
- **Description:** Get information about the state of a background task.
- **Request Type:** GET
- **Url parameters:**
    - `{id}`:(string) The ID of the task to get information about.
- **Response:**
  ```json
  {"state": "PENDING"}
  ```

## Accessing the Application

For Docker Compose, access the FastAPI application at [http://localhost:8000](http://localhost:8000).

For Kubernetes, access the FastAPI application using the NodePort service.

## Contributing

Feel free to contribute to this project. Fork the repository, make your changes, and submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
