# Use the official Python 3.9 image as the base
FROM python:3.9-slim

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 8000 for the Uvicorn server
EXPOSE 8000

# Run the command to start the Uvicorn server when the container is started
CMD ["uvicorn", "index:app", "--host", "0.0.0.0", "--port", "8000"]