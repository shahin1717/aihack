from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.database.connection import Base, engine
from app.routers.auth_router import router as auth_router
from app.routers.employee_router import router as employee_router
from app.routers.campaign_router import router as campaign_router
from app.routers.track_router import router as track_router
from app.routers.dashboard_router import router as dashboard_router
from app.routers.ai_router import router as ai_router


# Create all DB tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="PhishGuard API",
    description="A phishing simulation and training platform",
    version="1.0.0"
)


# ------------------------
# CORS (for your frontend)
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],       # change later if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ------------------------
# HEALTH CHECK
# ------------------------
@app.get("/health")
def health():
    return {"status": "ok"}


# ------------------------
# INCLUDE ROUTERS
# ------------------------
app.include_router(auth_router)
app.include_router(employee_router)
app.include_router(campaign_router)
app.include_router(track_router)
app.include_router(dashboard_router)
app.include_router(ai_router)
