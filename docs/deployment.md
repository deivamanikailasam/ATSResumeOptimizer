# Deployment

This guide covers how to deploy ATS Resume Optimizer for local use and production environments.

## Local Development

### Prerequisites

- Python 3.12 or later
- An OpenAI API key with access to `gpt-4o-mini`

### Setup

```bash
# Clone the repository
git clone https://github.com/<your-username>/ATSResumeOptimizer.git
cd ATSResumeOptimizer

# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (macOS/Linux)
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser
playwright install chromium

# Create environment file
echo OPENAI_API_KEY=sk-... > .env

# Run the app
streamlit run app.py
```

## Docker Deployment

### Dockerfile

```dockerfile
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libnss3 libnspr4 libatk1.0-0 libatk-bridge2.0-0 \
    libcups2 libdrm2 libxkbcommon0 libxcomposite1 \
    libxdamage1 libxrandr2 libgbm1 libpango-1.0-0 \
    libcairo2 libasound2 libxshmfence1 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && playwright install chromium

COPY . .

RUN mkdir -p memory/docs/generated

EXPOSE 8501

HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

ENTRYPOINT ["streamlit", "run", "app.py", \
    "--server.port=8501", \
    "--server.address=0.0.0.0", \
    "--server.headless=true"]
```

### Build and Run

```bash
docker build -t ats-resume-optimizer .

docker run -d \
    -p 8501:8501 \
    -e OPENAI_API_KEY=sk-... \
    -v $(pwd)/memory:/app/memory \
    --name ats-optimizer \
    ats-resume-optimizer
```

The app will be available at `http://localhost:8501`.

### Docker Compose

```yaml
services:
  app:
    build: .
    ports:
      - "8501:8501"
    environment:
      - OPENAI_API_KEY=${OPENAI_API_KEY}
    volumes:
      - ./memory:/app/memory
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8501/_stcore/health"]
      interval: 30s
      timeout: 10s
      retries: 3
```

```bash
# Start
docker compose up -d

# Stop
docker compose down
```

## Streamlit Community Cloud

1. Push the repository to GitHub.
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repository.
3. Set the main file path to `app.py`.
4. Add `OPENAI_API_KEY` to the app's **Secrets** in the Streamlit dashboard.

The repository includes a `packages.txt` that installs the system-level libraries Chromium needs. The app automatically downloads the Playwright Chromium binary on the first PDF export, so no extra setup is required.

## Environment Variables in Production

| Variable | Required | Notes |
|---|---|---|
| `OPENAI_API_KEY` | Yes | Set via `.env`, container env, or cloud secrets. Never commit to version control. |

## Reverse Proxy (Nginx)

If hosting behind Nginx:

```nginx
server {
    listen 80;
    server_name resume.example.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

Streamlit uses WebSockets, so the `Upgrade` and `Connection` headers are required.

## Production Considerations

### Security

- **Never commit `.env` or API keys** to version control.
- **Use environment variables** or secret managers (AWS Secrets Manager, Azure Key Vault, etc.) for API keys.
- **Restrict network access** if deploying internally — Streamlit does not have built-in authentication.
- **Use HTTPS** in production via a reverse proxy with TLS certificates.

### Performance

- **PDF generation** is the heaviest operation — each export launches a headless Chromium instance. On resource-constrained environments, expect 3–10 seconds per PDF.
- **LLM API calls** depend on OpenAI's response time. Budget 5–15 seconds per iteration, up to the configured max iterations.
- **Caching** — the Streamlit UI caches optimization results by input fingerprint. Re-exporting with a different theme/color skips the LLM entirely.

### Storage

- Generated PDFs are stored in `memory/docs/generated/`. The Streamlit web UI automatically cleans up generated PDFs and uploaded resumes on each new session start (page reload, server restart, new browser tab). Generated PDFs are also cleaned on regenerate.
- In a multi-user deployment, consider:
  - Using a unique subdirectory per session.
  - Mounting a persistent volume (Docker) or object storage.
  - Note that automatic cleanup only covers the single shared `generated/` directory. Concurrent users may interfere with each other's files.

### Monitoring

- Streamlit exposes a health endpoint at `/_stcore/health`.
- Monitor OpenAI API usage and rate limits via the [OpenAI dashboard](https://platform.openai.com/usage).
- Log subprocess failures from PDF export — stderr is captured and raised as `RuntimeError`.
