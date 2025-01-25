FROM python:3.9-slim

WORKDIR /app

# Copy the requirements file first to leverage Docker caching
COPY ./app/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the rest of the application code
COPY ./app /app

# Expose Flask app on port 5000
CMD ["python", "webhook_receiver.py"]
