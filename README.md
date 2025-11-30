ZeroPhish

AI-Powered Phishing Simulation & Employee Security Awareness Platform

📌 Live Pitch Deck:
https://www.canva.com/design/DAG6EMjJKX4/utMfN2hMYPh47URZBycwAQ/view?utm_content=DAG6EMjJKX4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hfcfcb6cc85

🚀 Overview

ZeroPhish is an AI-driven platform that helps companies test, measure, and improve employee resistance to phishing attacks.

The platform automates everything:
✓ AI-generated email bodies
✓ AI-generated subjects
✓ Phishing campaign scheduling
✓ Click & open tracking
✓ Admin dashboard
✓ SMTP email delivery
✓ Logging, reporting & analytics

ZeroPhish strengthens cybersecurity awareness while saving companies time, money, and risk.

✨ Features
AI-Powered Campaign Engine

AI-generated phishing email text

AI-generated subjects

Personalized email bodies per employee

Multi-recipient dispatch

Schedule campaigns in advance

Automatic logging & status tracking

Tracking System

Pixel-based open tracking

Link-based click tracking

Dashboard with analytics

Historical reports

SMTP Integration

Send campaigns using:

Gmail

Workplace

Corporate SMTP servers

Testing SMTP servers

Admin Management

Employee database

Departments

Email logs

Campaign performance

🧱 Tech Stack
Backend

FastAPI

Python 3

SQLAlchemy ORM

MySQL / PostgreSQL

JWT Authentication

SMTP email delivery

Tracking endpoints:

/track/open/{recipient_id}

/track/click/{recipient_id}?redirect=URL

Frontend

HTML

CSS

JavaScript

Responsive admin dashboard

📦 Project Structure
ZeroPhish/
│
├── app/
│   ├── routers/
│   │   ├── auth_router.py
│   │   ├── employee_router.py
│   │   ├── campaign_router.py
│   │   ├── department_router.py
│   │   ├── track_router.py
│   │   └── dashboard_router.py
│   ├── database/
│   │   ├── connection.py
│   │   └── models.py
│   ├── services/
│   │   ├── email_sender.py
│   │   ├── ai_generator.py
│   │   └── utils.py
│   ├── config.py
│   └── main.py
│
├── frontend/
│   ├── employees.html
│   ├── campaigns.html
│   ├── auth.html
│   ├── dashboard.html
│   ├── css/
│   └── js/
│
└── run.py

⚙️ Installation
1. Clone the repo
git clone https://github.com/yourusername/ZeroPhish.git
cd ZeroPhish

2. Create virtual environment
python -m venv .venv
source .venv/bin/activate   # Linux/macOS
.\.venv\Scripts\activate    # Windows

3. Install dependencies
pip install -r requirements.txt

4. Configure Environment

Create .env:

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your@gmail.com
SMTP_PASSWORD=yourpass
SMTP_FROM_EMAIL=your@gmail.com

DATABASE_URL=mysql+pymysql://root:pass@localhost/zerophish
JWT_SECRET=supersecret

5. Run
python run.py

🌐 Deployment
Render / Railway / AlwaysData

Expose port 8000

Use python run.py

Make sure DB is accessible

Add environment variables

Configure SMTP (App Password for Gmail)

🛡 Security Notes

Never use personal Gmail passwords

Use App Passwords or dedicated SMTP

Always run behind HTTPS in production

Limit who can access the admin dashboard

🧭 Roadmap
M1 — MVP Completed ✔

Backend, frontend, AI generator, tracking, SMTP sending.

M2 — Pilot Users

Deploy to 1–2 companies and gather data.

M3 — Integrations

Slack alerts, export reports, auto-training.

M4 — Scale

Subscription payments, multi-tenant accounts.

👥 Team

ZeroPhish was built for the Cybersecurity Hackathon 2025
by a team of developers passionate about AI + Security.