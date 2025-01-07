# Use Python image as base
FROM python:3.9-slim

# creating work directory
WORKDIR /app

# Copy the directory files into the container application
COPY . /app

# Installing denpendencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port by Flask
EXPOSE 5000

# Start Flask application
CMD ["python", "app.py"]
