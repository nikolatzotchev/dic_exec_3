# Base image
FROM python:3.8

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install the required packages
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Python code to the container
COPY . .

# Expose the port on which the Flask app will run
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]

