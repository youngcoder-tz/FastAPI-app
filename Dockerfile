FROM python:3.9-slim as builder

# 1. First stage - install build dependencies and download packages
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY requirements.txt .

# Create virtual environment and install packages
RUN python -m venv /opt/venv && \
    /opt/venv/bin/pip install --upgrade pip && \
    /opt/venv/bin/pip install --no-cache-dir -r requirements.txt

# 2. Second stage - create lightweight runtime image
FROM python:3.9-slim

# Copy only the virtual environment from builder
COPY --from=builder /opt/venv /opt/venv
COPY --from=builder /usr/bin/ffmpeg /usr/bin/ffmpeg

WORKDIR /app
COPY . .

# Use the virtual environment
ENV PATH="/opt/venv/bin:$PATH"
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]