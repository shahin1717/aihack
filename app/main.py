from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

from app.routers.auth_router import router as auth_router
from app.routers.employee_router import router as employee_router
from app.routers.campaign_router import router as campaign_router
from app.routers.track_router import router as track_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.ai_router import router as ai_router

from app.database.connection import engine
from app.database.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhishGuard API")

# --------------------------
# STATIC FRONTEND
# --------------------------

FRONTEND_DIR = os.path.join(os.path.dirname(__file__), "frontend")
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# ===== Serve real HTML files =====
@app.get("/auth.html", include_in_schema=False)
def serve_auth():
    return FileResponse(os.path.join(FRONTEND_DIR, "auth.html"))

@app.get("/employees.html", include_in_schema=False)
def serve_employees():
    return FileResponse(os.path.join(FRONTEND_DIR, "employees.html"))

@app.get("/campaigns.html", include_in_schema=False)
def serve_campaigns():
    return FileResponse(os.path.join(FRONTEND_DIR, "campaigns.html"))

@app.get("/dashboard.html", include_in_schema=False)
def serve_dashboard():
    return FileResponse(os.path.join(FRONTEND_DIR, "dashboard.html"))

# ===== ONLY ONE ROOT ROUTE =====
@app.get("/", include_in_schema=False)
def root():
    return FileResponse(os.path.join(FRONTEND_DIR, "auth.html"))

# --------------------------
# CORS
# --------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------------
# ROUTERS (THE IMPORTANT PART)
# --------------------------
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(campaign_router)
app.include_router(track_router)
app.include_router(dashboard_router)
app.include_router(ai_router)

# --------------------------
# Health check
# --------------------------
@app.get("/health")
def health():
    return {"status": "ok"}
