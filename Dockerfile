# Use a lightweight Python image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the project files and .env into the container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose a port (if necessary for external interaction)
EXPOSE 8000

# Set the entrypoint to run the Python script with arguments
CMD ["python", "main.py"]