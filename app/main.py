from fastapi import FastAPI
from app.routers import auth_router, employee_router, campaign_router, track_router, ai_router, dashboard_router
from app.database.connection import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhishGuard API", version="1.0.0")

# Include routers
app.include_router(auth_router.router)
app.include_router(employee_router.router)
app.include_router(campaign_router.router)
app.include_router(track_router.router)
app.include_router(ai_router.router)
app.include_router(dashboard_router.router)


@app.get("/health")
def health_check():
    return {"status": "ok"}

