# Project Guidelines

## Code Style
Python: Follow PEP 8, use type hints where appropriate. Reference [src/app.py](src/app.py) for FastAPI patterns.

## Architecture
Simple 2-tier structure: FastAPI backend with in-memory storage, vanilla JS + HTML/CSS frontend. See [src/README.md](src/README.md) for API details and endpoints.

## Build and Test
Install dependencies: `pip install -r requirements.txt`  
Start server: `python src/app.py`  
Test: `pytest` (pytest.ini configured, but no test files exist yet)

## Conventions
This is a GitHub Copilot skills learning repository. Follow the exercise steps in `.github/steps/` for guided progression. Intentional bugs exist for practice (e.g., duplicate signups allowed, no validation). Data is in-memory only - resets on server restart.