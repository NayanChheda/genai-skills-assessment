# Multi-stage build for minimal image size
# Build stage
FROM python:3.11-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency files
COPY pyproject.toml requirements.txt ./

# Create virtual environment and install dependencies
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --upgrade pip && \
    pip install -e ".[dev]" --no-cache-dir

# Runtime stage
FROM python:3.11-slim as runtime

WORKDIR /app

# Install runtime dependencies (git needed for scoring)
RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONIOENCODING=utf-8

# Default command: run tests
CMD ["pytest", "-v"]

# Alternative commands:
# Run scoring: docker run assessment python automated_scoring.py
# Run specific tests: docker run assessment pytest tests/unit -v
# Interactive shell: docker run -it assessment bash
