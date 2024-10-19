__all__ = [
    "MONGODB_URI",
    "logger",
    "JWT_SECRET",
    "HOST_URL",
    "HOST_PORT",
    "FRONTEND_HOST",
]

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables
MONGODB_URI = os.getenv("MONGODB_URI")

JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_key")

HOST_URL = os.getenv("HOST_URL", "localhost")

FRONTEND_HOST = os.getenv("FRONTEND_HOST", "localhost")

HOST_PORT = int(os.getenv("HOST_PORT") or 8000)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# Fixing a "bycript issue"
logging.getLogger("passlib").setLevel(logging.ERROR)
