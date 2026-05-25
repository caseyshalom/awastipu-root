import os
import sys

# Pindah ke direktori backend agar uvicorn dapat menemukan .env dan resources
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
os.chdir(backend_dir)
sys.path.insert(0, backend_dir)

from main import app
