import os
from dotenv import load_dotenv

# Load environment variables from a .env file if present
load_dotenv()

# Define the backend API URL
# Defaults to localhost:8000 for local development, but can be overridden by Railway/production environments
API_BASE_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")