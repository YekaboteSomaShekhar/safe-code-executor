# Use official Python base image
FROM python:3.11-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project files
COPY . .

# Expose Flask port
EXPOSE 5000

# Use Gunicorn as the production server
# (bind to 0.0.0.0 so Docker can access it)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
