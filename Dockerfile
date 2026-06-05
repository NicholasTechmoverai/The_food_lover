# Stage 1: Build the frontend
FROM node:20-slim AS builder

WORKDIR /app

# COPY 1: Copy the entire project to compile the frontend
COPY . .

# Install dependencies and build
RUN npm ci && npm run build

# Stage 2: Python Runner
FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# COPY 2: Copy the backend source files from the builder stage
COPY --from=builder /app/backend ./backend

# COPY 3: Copy the compiled frontend dist folder from the builder stage
COPY --from=builder /app/dist ./dist

# Install python dependencies and create verification logs
RUN pip install --no-cache-dir -r backend/requirements.txt \
    && mkdir -p /logs/verifier \
    && printf "0\n" > /logs/verifier/reward.txt

WORKDIR /app/backend

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=5 \
  CMD python -c "import urllib.request, os; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8000') + '/health', timeout=2)"

CMD ["sh", "-c", "python -m uvicorn app:socket_app --host 0.0.0.0 --port ${PORT:-8000}"]
