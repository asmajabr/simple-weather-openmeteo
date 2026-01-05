# 1) Standard library
import os

# 2) Third-party
import uvicorn

# 3) Local/application
from src.app import app



if __name__ == "__main__":
    # Default to loopback in dev/CI; set HOST=0.0.0.0 in production via env
    host = os.getenv("HOST", "127.0.0.1")
    # String default, then cast to int
    port = int(os.getenv("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)
