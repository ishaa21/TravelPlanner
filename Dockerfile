# ── Base: Node 20 + Python 3 ──────────────────────────────────────────────────
# We need Node for `npx @modelcontextprotocol/server-google-maps`
# and Python for ADK + FastAPI.
FROM node:20-slim

# Install Python & pip
RUN apt-get update && \
    apt-get install -y python3 python3-pip python3-venv curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# ── Pre-cache the MCP server package (speeds up first run) ───────────────────
RUN npm install -g @modelcontextprotocol/server-google-maps

# ── Python dependencies ───────────────────────────────────────────────────────
COPY requirements.txt .
RUN python3 -m pip install --no-cache-dir --break-system-packages -r requirements.txt

# ── Application code ──────────────────────────────────────────────────────────
COPY . .

# Ensure package is importable
RUN touch __init__.py 2>/dev/null || true

# ── Runtime config ────────────────────────────────────────────────────────────
EXPOSE 8080
ENV PORT=8080
ENV PYTHONUNBUFFERED=1

CMD ["python3", "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
