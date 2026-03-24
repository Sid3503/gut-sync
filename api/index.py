import sys
import os

# Add backend folder to Python path
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "gut-health-alpha")
)

# Import the FastAPI app
from src.web.api import app

# Mount the app at /api so Vercel routes /api/* correctly to FastAPI
# Vercel passes the full path (e.g. /api/webhook/incoming) to this function.
# Setting root_path tells FastAPI it lives under /api, so /api/health → /health internally.
app.root_path = "/api"
