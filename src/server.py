
# src/server.py
import os

import uvicorn
from src.app import app

if __name__ == "__main__":
    host = os.getenv("HOST", "127.0.0.1")  # default avoids B104
    port = int(os.getenv("PORT", "8000"))  # string default, then cast
    uvicorn.run(app, host=host, port=port)
