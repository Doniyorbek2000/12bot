FROM python:3.11-slim

WORKDIR /app

# Install system dependencies needed for python packages (compiling C extensions if any)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Run bot by default
CMD ["python", "-m", "app.main"]
