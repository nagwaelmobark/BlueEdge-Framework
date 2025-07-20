# BlueEdge Framework - Docker Configuration
# Base image with Python 3.9 (stable and well-tested)
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8

# Install system dependencies for Arabic text support and NLTK
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first (for better Docker layer caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Download NLTK data (required for text processing)
RUN python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords')"

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data results logs

# Set permissions
RUN chmod +x scripts/*.py 2>/dev/null || true

# Expose port for web interface (if needed later)
EXPOSE 8080

# Health check
HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3 \
    CMD python -c "import sys; sys.exit(0)" || exit 1

# Default command - run the quick test
CMD ["python", "quick_test.py"]

# Alternative commands you can use:
# docker run blueedge-framework python scripts/validate_framework.py
# docker run blueedge-framework python -m pytest tests/
# docker run -it blueedge-framework /bin/bash 
