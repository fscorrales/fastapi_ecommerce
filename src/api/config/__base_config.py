__all__ = [
    "PORT",
    "MONGODB_URI",
    "logger",
]

import logging
import os

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set environment variables
PORT = os.getenv("PORT", "3000")
MONGODB_URI = os.getenv(
    "MONGODB_URI", "mongodb://127.0.0.1:27017/bootcamp_eCommerce_app"
)

logger = logging.getLogger("uvicorn")
logger.setLevel(logging.DEBUG)
