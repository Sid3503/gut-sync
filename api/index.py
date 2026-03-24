import sys
import os

# Add backend folder to Python path
sys.path.append(
    os.path.join(os.path.dirname(__file__), "..", "gut-health-alpha")
)

from src.web.api import app
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class StripAPIPrefixMiddleware(BaseHTTPMiddleware):
    """Strip /api prefix from paths so FastAPI routes match correctly on Vercel.

    Vercel routes /api/* to this function with the full path intact.
    FastAPI registers routes without /api prefix (e.g. /webhook/incoming),
    so we strip /api before FastAPI sees the request.
    """

    async def dispatch(self, request: Request, call_next):
        path: str = request.scope.get("path", "")
        if path.startswith("/api"):
            request.scope["path"] = path[4:] or "/"
        return await call_next(request)


app.add_middleware(StripAPIPrefixMiddleware)
