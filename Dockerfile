# Multi-stage/cached production Dockerfile for GridWise LLM API
FROM python:3.11-slim AS base

# Install system utilities (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Create dedicated non-root application user
RUN useradd -m -u 1000 -s /bin/bash appuser

WORKDIR /app

# Copy dependency specifications first to leverage Docker layer caching
COPY requirements.txt .

# Install dependencies into system Python
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY src/ /app/src/
COPY samples/ /app/samples/
COPY scripts/ /app/scripts/

# Set ownership to appuser
RUN chown -R appuser:appuser /app

USER appuser

# Environment configurations
ENV PORT=3000 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

EXPOSE 3000

# Docker healthcheck against canonical GET /health endpoint
HEALTHCHECK --interval=15s --timeout=5s --start-period=10s --retries=3 \
  CMD curl -f http://localhost:3000/health || exit 1

# Production server entrypoint
CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "3000", "--workers", "2", "--timeout-keep-alive", "30"]
