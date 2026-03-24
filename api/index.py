import sys
import os

# Add backend path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "gut-health-alpha"))

from src.web.api import app
