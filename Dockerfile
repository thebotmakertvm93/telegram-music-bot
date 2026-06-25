# Use a lightweight Python image
FROM python:3.10-slim

# Install FFmpeg (Crucial for PyTgCalls)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your bot's code
COPY . .

# Run the bot
CMD ["python", "main.py"]
