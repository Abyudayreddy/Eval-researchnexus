import os
os.environ["FOR_DISABLE_CONSOLE_CTRL_HANDLER"] = "1"
os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import api_router
from app.db.session import engine, Base, db_url
import app.models.user
import app.models.paper
import app.models.workspace
import app.models.search_experiment
import app.models.search_history

from sqlalchemy import text

# Create tables for dev
Base.metadata.create_all(bind=engine)

# Auto-migrate profile columns for local dev
try:
    with engine.begin() as conn:
        existing_cols = {row[1] for row in conn.execute(text("PRAGMA table_info(users)")).fetchall()} if "sqlite" in db_url else set()
        cols_to_add = [
            ("title", "VARCHAR"), ("institution", "VARCHAR"), ("bio", "TEXT"),
            ("location", "VARCHAR"), ("website", "VARCHAR"), ("orcid", "VARCHAR"), 
            ("google_scholar", "VARCHAR")
        ]
        for col_name, col_type in cols_to_add:
            if not existing_cols or col_name not in existing_cols:
                try:
                    conn.execute(text(f"ALTER TABLE users ADD COLUMN {col_name} {col_type}"))
                except Exception:
                    pass # Column exists
except Exception as e:
    print("Auto-migration skipped:", e)

# Seed default demo user for instant login
try:
    from app.db.session import SessionLocal
    from app.models.user import User
    from app.core.security import get_password_hash
    db = SessionLocal()
    try:
        demo_user = db.query(User).filter(User.email == "demo@researchnexus.ai").first()
        if not demo_user:
            demo_user = User(
                id="default_user",
                email="demo@researchnexus.ai",
                name="Demo Researcher",
                hashed_password=get_password_hash("demo1234"),
                is_active=True
            )
            db.add(demo_user)
            db.commit()
            print("Seeded default demo user: demo@researchnexus.ai / demo1234")
    finally:
        db.close()
except Exception as seed_err:
    print("Seed user skipped:", seed_err)

app = FastAPI(title=settings.PROJECT_NAME)

origins = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1)(:\d+)?",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix=settings.API_V1_STR)

@app.get("/")
def root():
    return {"message": f"Welcome to {settings.PROJECT_NAME} API"}

@app.get("/health")
@app.get("/api/health")
def health_check():
    return {"status": "ok"}
