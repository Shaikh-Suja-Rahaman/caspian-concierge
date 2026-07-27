# Use an official Python runtime as a lightweight base image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port 10000 for the dummy web server (Render health checks)
EXPOSE 10000

# Run the bot
CMD ["python", "main.py"]
