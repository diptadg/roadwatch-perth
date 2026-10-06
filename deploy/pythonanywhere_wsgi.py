# PythonAnywhere WSGI entry point for RoadWatch Perth.
#
# Copy this file's contents into the WSGI configuration file linked from the
# PythonAnywhere Web tab (/var/www/diptadg_pythonanywhere_com_wsgi.py),
# replacing everything that is there. See documentation/DEPLOYMENT.md.
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

PROJECT_DIR = Path.home() / "roadwatch-perth"

if str(PROJECT_DIR) not in sys.path:
    sys.path.insert(0, str(PROJECT_DIR))

load_dotenv(PROJECT_DIR / ".env")

if not os.getenv("SECRET_KEY"):
    raise RuntimeError(f"SECRET_KEY is not set. Add it to {PROJECT_DIR / '.env'}.")

from app import app as application  # noqa: E402
