# src/server.py

# Standard library
import os

# Third-party
import uvicorn

# Local/application
from src.app import app

# If there is other server content below, keep it unchanged.
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.environ.get("PORT", 8000)))
