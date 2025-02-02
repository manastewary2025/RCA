# Use an official Python runtime as a base image
FROM python:3.12.7-slim

# Install setuptools, distutils
RUN pip install --no-cache-dir --upgrade setuptools

# Create a group and user
RUN groupadd --gid 2000 app && \
    useradd -u 1000 -g app -m -s /bin/bash app


# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Change the ownership of the application directory to the new user
RUN chown -R app:app /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Switch to the new user
USER app

# Expose port 5000 for the Flask app
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=./chatbot-api/api/index.py
ENV FLASK_ENV=development

HEALTHCHECK CMD curl --fail http://localhost:5000 || exit 1

# Command to run the Flask app with Socket.IO support
CMD ["flask", "run", "--host=0.0.0.0"]
