
# Simple Weather API (Open-Meteo)

A minimal FastAPI service that wraps the **Open-Meteo** weather API to provide current, daily, and
hourly endpoints. Built to comply with the assignment "Implementación de un Pipeline de Entrega
Continua y Calidad Automatizada".

## Endpoints
- `GET /health` → liveness
- `GET /weather/current?lat=&lon=&tz=` → current weather + `weather_text` (human-readable)
- `GET /weather/forecast?lat=&lon=&days=&tz=` → daily max/min temperature & precipitation (≤ 7 days)
- `GET /weather/hourly?lat=&lon=&vars=&tz=` → selected hourly variables for ~24h

## Run locally
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn src.app:app --reload --port 8000
```
Open http://localhost:8000/docs

## Tests (Q1/Q2) & Coverage
```bash
pytest
```
- Unit tests: mapping of Open‑Meteo weather codes → text.
- Integration tests: endpoints with **mocked HTTP** (no network).
- Coverage: generated as `coverage.xml`.

## CI/CD
- **CI** (`.github/workflows/ci.yml`): Ruff (lint), PyTest (tests+coverage), Bandit (SAST), Docker build.
- **CodeQL** (`.github/workflows/codeql.yml`): Python security analysis.
- **Dependabot** (`.github/dependabot.yml`): weekly pip updates.
- **Deploy** (`.github/workflows/deploy.yml`): On push to `main`, triggers **Render Deploy Hook**.

### Configure deployment (Render)
1. Create a **Web Service** in Render, connect your GitHub repo (Dockerfile will be detected).
2. In the service **Settings → Deploy Hooks → Create Hook** and copy the URL.
3. In GitHub repo **Settings → Secrets and variables → Actions → New repository secret**:
   - Name: `RENDER_DEPLOY_HOOK`
   - Value: the hook URL from Render.
4. Push/merge to `main` → GitHub Actions calls the hook → Render deploys.

## Branch protection (suggested checks)
Require before merging to `main`:
- `CI / lint` (ruff)
- `CI / tests` (pytest + coverage)
- `CI / bandit` (security)
- `CI / docker-build` (image compiles)
- `CodeQL / Analyze (Python)`

## DORA Lead Time
Show PR merge time → CI green → **deploy completed** (Render dashboard). Compute lead time.

## Sources
- Open‑Meteo docs and parameters: https://open-meteo.com/en/docs
- Open‑Meteo public repo (no API key, CORS): https://github.com/open-meteo/open-meteo
