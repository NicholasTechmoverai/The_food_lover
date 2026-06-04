FROM python:3.11.9-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=8000

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends nodejs npm \
    && rm -rf /var/lib/apt/lists/*

COPY backend/requirements.txt package.json package-lock.json ./

RUN pip install --no-cache-dir -r requirements.txt \
    && npm ci

COPY backend ./backend
COPY src public index.html vite.config.js tailwind.config.js bellakitchenware.jpg ./

RUN npm run build \
    && mkdir -p /logs/verifier \
    && printf "0\n" > /logs/verifier/reward.txt

WORKDIR /app/backend

EXPOSE 8000

HEALTHCHECK --interval=10s --timeout=3s --start-period=30s --retries=5 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8000/health', timeout=2)"

CMD ["uvicorn", "app:socket_app", "--host", "0.0.0.0", "--port", "8000"]
