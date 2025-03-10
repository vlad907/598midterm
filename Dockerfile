# Use an official Python runtime as a parent image
FROM python:3.12.9

# Set environment variables (optional)
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files into the container
COPY . /app/

# Run the development server on 0.0.0.0:8000 so it is accessible externally
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
