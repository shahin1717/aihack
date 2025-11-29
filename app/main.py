import os
from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

app = FastAPI(title="PhishGuard API")

BASE_DIR = os.path.dirname(__file__)
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
PAGES_DIR = os.path.join(FRONTEND_DIR, "pages")

# Serve CSS/JS
app.mount("/static", StaticFiles(directory=FRONTEND_DIR), name="static")

# Serve pages
@app.get("/")
def index():
    return FileResponse(os.path.join(PAGES_DIR, "index.html"))

@app.get("/auth.html")
def auth_page():
    return FileResponse(os.path.join(PAGES_DIR, "auth.html"))

@app.get("/employees.html")
def employees_page():
    return FileResponse(os.path.join(PAGES_DIR, "employees.html"))

@app.get("/campaigns.html")
def campaigns_page():
    return FileResponse(os.path.join(PAGES_DIR, "campaigns.html"))

@app.get("/dashboard.html")
def dashboard_page():
    return FileResponse(os.path.join(PAGES_DIR, "dashboard.html"))
