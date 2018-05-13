# Use an official Python runtime as a parent image
FROM python:3

# Set the working directory to /app
ADD requirements.txt /app/
WORKDIR /app
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /app
ADD . /app
