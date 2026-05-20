import sys
import logging
from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from app.api.drops import router as drops_router

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)

app = FastAPI(title="Data Processing App", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(drops_router, prefix="/api/v1")

# Serve the compiled frontend when the dist directory is present (packaged build).
# In a PyInstaller bundle, data files land in sys._MEIPASS, not relative to __file__.
if hasattr(sys, "_MEIPASS"):
    _frontend_dist = Path(sys._MEIPASS) / "frontend" / "dist"
else:
    _frontend_dist = Path(__file__).parent.parent / "frontend" / "dist"

if _frontend_dist.is_dir():
    app.mount("/", StaticFiles(directory=str(_frontend_dist), html=True), name="frontend")
