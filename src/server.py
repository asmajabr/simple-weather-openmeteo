# src/server.py
import os
import uvicorn
from src.app import app

if __name__ == "__main__":
    # Use string defaults for os.environ.get(...) (ruff/PLW1508 wants str | None).
    # Make host configurable so we avoid binding to all interfaces by default,
    # which Bandit flags as a medium-risk item (B104).
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
