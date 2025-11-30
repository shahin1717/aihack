🛡️ ZeroPhish

AI-powered phishing simulation & employee awareness training platform

ZeroPhish is a cybersecurity tool that helps companies test, measure, and improve their employees’ resistance to phishing attacks.
It sends AI-generated phishing emails, tracks interactions, and provides actionable analytics.

🚀 Features

AI-generated subjects + HTML phishing templates

Multi-recipient campaign sending

SMTP support (Gmail, corporate, custom SMTP)

Email open tracking via invisible pixel

Click tracking with redirect logging

Department & employee management

Awareness scoring

Analytics dashboard

Secure authentication (JWT)

Modern FastAPI backend + responsive JS frontend

🛠 Tech Stack
Backend

FastAPI

Python 3.10+

SQLAlchemy ORM

MySQL / PostgreSQL

JWT Authentication

SMTP mail sending

AI providers (OpenAI / Gemini)

Frontend

HTML / CSS / JavaScript

Responsive admin interface

🏗️ Architecture
┌─────────────────┐     ┌────────────────────┐     ┌──────────────────┐
│   GitHub Repo   │───▶ │ GitHub Actions CI  │───▶ │ Render Deployment │
└─────────────────┘     └────────────────────┘     └──────────────────┘
                              │                             │
                              ▼                             ▼

                    ┌─────────────────────┐    ┌─────────────────────┐
                    │     FastAPI API     │    │     Frontend UI      │
                    │ - Auth (JWT)        │    │ - Dashboard          │
                    │ - Employees         │    │ - Campaign builder   │
                    │ - Departments       │    │ - Tracking views     │
                    │ - Campaigns         │    └─────────────────────┘
                    │ - Tracking          │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │     SMTP Server     │
                    │ Gmail / Workplace   │
                    │ Custom SMTP         │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    Database (SQL)   │
                    │ employees           │
                    │ campaigns           │
                    │ recipients          │
                    │ open/click logs     │
                    └─────────────────────┘

📦 Installation

Clone the repository:

git clone https://github.com/your-username/zerophish.git
cd zerophish


Create virtual environment:

python -m venv .venv
source .venv/bin/activate     # Linux/Mac
# OR
.venv\Scripts\Activate.ps1    # Windows


Install dependencies:

pip install -r requirements.txt


Run the server:

python run.py


Open in browser:
http://127.0.0.1:8000

⚙️ Environment Variables

Create a .env file:

SECRET_KEY=your-secret
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-password
DB_URL=mysql+pymysql://user:pass@localhost/zerophish
OPENAI_API_KEY=xxxx

✉️ Usage
Sending a phishing campaign (example)
from app.email_sender import send_campaign_emails
from app.database.connection import get_db

db = get_db()

send_campaign_emails(
    db=db,
    campaign=my_campaign,
    base_url="https://yourdomain.com",
    redirect_url="https://example.com"
)

AI-generated email example
<p>Dear Employee,</p>
<p>We detected unusual login activity. Please verify your account.</p>
<a href="https://yourdomain.com/track/click/12">Verify Now</a>
<img src="https://yourdomain.com/track/open/12" width="1" height="1" />

🔌 Tracking Endpoints
GET /track/open/{recipient_id}
Logs an email open event.

GET /track/click/{recipient_id}?redirect=https://site.com
Logs a click event and redirects user.

📁 Project Structure
zerophish/
├── app/
│   ├── routers/
│   ├── database/
│   ├── templates/
│   ├── static/
│   └── email_sender.py
├── run.py
├── requirements.txt
└── README.md

📊 Dashboard Highlights

Sent emails

Open rate

Click rate

Per-department awareness score

Employee-level event history

🤝 Contributing

Pull requests are welcome!

To contribute:

git checkout -b feature/improvement
git commit -m "Improved campaign logic"
git push origin feature/improvement


Please open an issue for big changes.
