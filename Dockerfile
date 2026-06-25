# Use a specific, stable Python image version with precise Debian build environments
FROM python:3.9-slim-bullseye

# Install FFmpeg and required compilation tools for C++ audio components
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Upgrade pip first to ensure proper dependency resolution
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code
COPY . .

# Run the bot
CMD ["python", "main.py"]
Use code with caution.
