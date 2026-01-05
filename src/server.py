# src/server.py

# Standard library
import os

# Third-party
import uvicorn

# Local/application
from src.app import app

# (rest of your server.py content follows unchanged)




if __name__ == "__main__":
    # Default to loopback in dev/CI; set HOST=0.0.0.0 in production via env
    host = os.getenv("HOST", "127.0.0.1")
    # String default, then cast to int
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
