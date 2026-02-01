# ATLAS AI Telegram Bot - Docker for Render
# Multi-User Media Edition with complete AI capabilities

FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for media processing
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    ffmpeg \
    libffi-dev \
    libssl-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY atlas_ai_telegram_bot.py .
COPY media_handler.py .

# Create non-root user for security
RUN useradd -m -u 1000 botuser && chown -R botuser:botuser /app
USER botuser

# Expose port for health checks
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD python -c "import requests; requests.get('https://api.telegram.org/bot' + os.getenv('TELEGRAM_BOT_TOKEN', '') + '/getMe', timeout=5)" || exit 1

# Run the bot
CMD ["python", "atlas_ai_telegram_bot.py"]
