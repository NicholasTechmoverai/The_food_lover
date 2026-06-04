import os
from pathlib import Path

import pytest

ROOT_DIR = Path(__file__).resolve().parents[3]
BACKEND_DIR = ROOT_DIR / "backend"


@pytest.fixture(autouse=True, scope="session")
def static_directories():
    (ROOT_DIR / "dist" / "assets").mkdir(parents=True, exist_ok=True)
    (BACKEND_DIR / "uploads").mkdir(parents=True, exist_ok=True)
    os.chdir(BACKEND_DIR)
