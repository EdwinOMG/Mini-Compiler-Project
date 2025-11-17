FROM python:3.12-slim

# Install system-level Graphviz
RUN apt-get update && apt-get install -y graphviz

# Create app directory
WORKDIR /app

# Copy everything
COPY . .

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 10000

# Run your app with waitresss
CMD ["waitress-serve", "--host=0.0.0.0", "--port=10000", "app:app"]