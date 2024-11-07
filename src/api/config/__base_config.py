__all__ = [
    "MONGODB_URI",
    "logger",
    "JWT_SECRET",
    "HOST_URL",
    "HOST_PORT",
    "FRONTEND_HOST",
    "UNSPLASH_ACCESS_KEY",
]

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables
MONGODB_URI = os.getenv(
    "MONGODB_URI", "mongodb://127.0.0.1:27017/bootcamp_eCommerce_app"
)

JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_key")

HOST_URL = os.getenv("HOST_URL", "localhost")

FRONTEND_HOST = os.getenv("FRONTEND_HOST", "localhost")

HOST_PORT = int(os.getenv("HOST_PORT") or 8000)

UNSPLASH_ACCESS_KEY = os.getenv("UNSPLASH_ACCESS_KEY")

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)

# Fixing a "bycript issue"
logging.getLogger("passlib").setLevel(logging.ERROR)
