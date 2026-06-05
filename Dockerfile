# Stage 1: Build the frontend static assets
FROM node:20-slim AS frontend-builder
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci
COPY src ./src
COPY public ./public
COPY index.html vite.config.js tailwind.config.js bellakitchenware.jpg ./
RUN npm run build

# Stage 2: Final runtime container
FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

# Install Python requirements
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend application
COPY backend ./backend

# Copy compiled frontend assets from builder stage
COPY --from=frontend-builder /app/dist ./dist

# Copy bellakitchenware.jpg just in case it is dynamically referenced by the backend
COPY bellakitchenware.jpg ./

# Create verifier reward file
RUN mkdir -p /logs/verifier \
    && printf "0\n" > /logs/verifier/reward.txt

WORKDIR /app/backend

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=5 \
  CMD python -c "import urllib.request, os; urllib.request.urlopen('http://127.0.0.1:' + os.environ.get('PORT', '8000') + '/health', timeout=2)"

CMD ["sh", "-c", "python -m uvicorn app:socket_app --host 0.0.0.0 --port ${PORT:-8000}"]
