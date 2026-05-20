FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy both the tool definitions and the API wrapper
COPY server.py .
COPY api_server.py .

ENV PORT=8080

# Run the HTTP API server
CMD ["python", "api_server.py"]