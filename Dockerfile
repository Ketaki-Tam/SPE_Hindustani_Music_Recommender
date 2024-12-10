# Base image
FROM python:3.8-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . /app/

# Expose the port
EXPOSE 8000

#Run tests
RUN python manage.py test

# Run the server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
