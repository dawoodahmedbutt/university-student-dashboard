# Student-data-system
group coursework for WM9QF:Programming for Artificial Intelligence

Student Data System — Run Instructions

Overview
- This repository contains a FastAPI backend and a Streamlit frontend for a student data system.

Prerequisites
- Python 3.10+ (macOS zsh)
- Git (optional)

Quick setup (dev)
1. Create and activate a virtual environment (from repo root):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

2. Install backend dependencies (FastAPI, Uvicorn, SQLAlchemy, etc.):

```bash
pip install fastapi uvicorn sqlalchemy pydantic
```

3. Install frontend dependencies (Streamlit + plotting libs):

```bash
pip install -r frontend/requirements.txt
```

Notes: If you prefer, install all dependencies in one step by adding backend packages to a top-level `requirements.txt`.

Database initialization
- The project uses SQLite by default. The database file is `university.db` in the project root.
- To create the schema and seed sample data run the seeder located in `src/seed_university_db.py`.

Run:

```bash
# from repo root (recommended)
python src/seed_university_db.py
# or to reset and reseed
python src/seed_university_db.py --reset
```

This will create `university.db` in the repo root and populate it with sample data.

Run the backend (FastAPI)
- Start the API from the repository root so imports using the `src` package resolve correctly.

```bash
# from repo root
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- API docs will be available at: `http://127.0.0.1:8000/docs`.

Run the frontend (Streamlit)
- The Streamlit app lives under `frontend/src`. It uses local imports (e.g., `components`, `pages`) that require the current working directory to be `frontend/src` or `PYTHONPATH` to include `frontend/src`.

Option A — change directory and run:

```bash
cd frontend/src
streamlit run app.py
```

Option B — run from repo root by setting `PYTHONPATH`:

```bash
PYTHONPATH=frontend/src streamlit run frontend/src/app.py
```

- Streamlit UI will be available at `http://localhost:8501` by default.

Troubleshooting
- Import errors in Streamlit: ensure you run from `frontend/src` or set `PYTHONPATH` as shown above.
- Database errors: ensure `university.db` exists (run the seeder). The DB engine is in `src/Data_Access_Layer/DB.py` and uses `sqlite:///university.db` by default.
- Port conflicts: change the port in the `uvicorn` or `streamlit` command (e.g., `--port 8001` or `--server.port 8502`).

Recommended dev workflow
- Use one terminal for backend (uvicorn) and another for frontend (streamlit).
- Keep the virtual environment activated in both terminals.

Production notes
- SQLite is convenient for development but consider PostgreSQL or MySQL for production. Update `src/Data_Access_Layer/DB.py` or add an environment variable to configure the DB URL.
- Use a proper ASGI server with process management (e.g., `gunicorn -k uvicorn.workers.UvicornWorker`) behind a reverse proxy for production deployment.

Files & entry points
- Backend entry: `main.py` (FastAPI app)
- DB config: `src/Data_Access_Layer/DB.py`
- DB seeder: `src/seed_university_db.py`
- Frontend entry: `frontend/src/app.py` (Streamlit)

Next steps
- (Optional) Add a top-level `requirements.txt` listing backend and frontend deps.
- (Optional) Make `DATABASE_URL` configurable via environment variables.
- (Optional) Add a `Makefile` or `scripts` to automate setup commands.

If you'd like, I can:
- add a `requirements.txt` with exact versions,
- add a small `Makefile` to run the common commands,
- or update `src/Data_Access_Layer/DB.py` to read `DATABASE_URL` from env.

