# Use an official Python image as base
FROM python:3.10-slim

# Define build-time argument with a default
ARG APP_NAME="DockerAppProduct"

# Set environment variable using the ARG
ENV APP_NAME=${APP_NAME}

# Set the working directory inside the container
WORKDIR /app

# Copy app files to container
COPY . .


# Install Python dependencies
RUN pip install --no-cache-dir -r requirments.txt

# Expose the port the app runs on
EXPOSE 8000

# Define the default command to run the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

