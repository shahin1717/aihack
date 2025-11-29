# PhishGuard

A FastAPI-based phishing awareness training platform.

## Setup

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure environment variables (optional):
Create a `.env` file with:
```
DATABASE_URL=sqlite:///./phishguard.db
JWT_SECRET_KEY=your-secret-key-here
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM_EMAIL=your-email@gmail.com
```

3. Run the server:
```bash
python run.py
```

The API will be available at `http://localhost:8000`

## API Documentation

Once running, visit:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Endpoints

- `GET /health` - Health check
- `POST /auth/login` - Admin login
- `POST /employees/add` - Create employee (protected)
- `GET /employees/` - List employees (protected)
- `POST /campaign/create` - Create campaign (protected)
- `POST /campaign/{id}/send` - Send campaign emails (protected)
- `GET /campaign/` - List campaigns (protected)
- `GET /track/open/{campaign_id}/{employee_id}.png` - Track email open
- `GET /track/click/{campaign_id}/{employee_id}` - Track link click
- `GET /track/report/{campaign_id}/{employee_id}` - Track phishing report
- `POST /ai/generate-email` - Generate phishing email (protected)
- `GET /dashboard/campaign/{id}/stats` - Campaign statistics (protected)
- `GET /dashboard/overview` - Overall statistics (protected)

