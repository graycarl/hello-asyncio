FROM python:3.10

# Install nginx
RUN apt-get update && apt-get install -y nginx

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY src /app

# Add entrypoint.sh
COPY entrypoint.sh /app
RUN chmod +x /app/entrypoint.sh
ENTRYPOINT ["/app/entrypoint.sh"]
