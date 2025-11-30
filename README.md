🛡️ ZeroPhish — AI-Powered Phishing Simulation & Security Awareness Platform

ZeroPhish is a modern cybersecurity platform designed to help organizations test, train, and protect employees against phishing attacks.
It generates AI-crafted phishing emails, tracks opens & clicks, and provides real-time security insights — all through a simple, effective dashboard.

🔗 Pitch Deck:
https://www.canva.com/design/DAG6EMjJKX4/utMfN2hMYPh47URZBycwAQ/view?utm_content=DAG6EMjJKX4&utm_campaign=designshare&utm_medium=link2&utm_source=uniquelinks&utlId=hfcfcb6cc85

✨ Features
🤖 AI-Generated Phishing Emails

ZeroPhish uses AI to craft realistic, scenario-based phishing templates — personalized per employee.

📊 Real-Time Tracking

Open-tracking pixel

Click-tracking redirect

Live analytics dashboard

Campaign performance scoring

Employee vulnerability index

🧑‍💼 Employee & Department Management

Admin panel includes:

Departments

Employees

Recipient lists

Personalized email bodies (AI optional)

🎯 Phishing Campaign Simulator

Customizable HTML email templates

AI body + subject generation

Scheduling

Multi-recipient dispatch

Automated logging

📩 SMTP Integration

Send from real corporate email or test SMTP:

Gmail

Workplace

Custom SMTP servers

🧱 Tech Stack
Backend

FastAPI

Python

SQLAlchemy ORM

MySQL / PostgreSQL

JWT Authentication

SMTP (email sending)

Tracking endpoints (/track/open, /track/click)

Frontend

HTML/CSS/JS

Responsive admin interface

Live monitoring components

⚙️ Installation
1️⃣ Clone Repo
git clone https://github.com/yourname/zerophish.git
cd zerophish

2️⃣ Create Virtual Environment
python -m venv .venv
source .venv/bin/activate        # macOS/Linux
.venv\Scripts\activate           # Windows

3️⃣ Install Dependencies
pip install -r requirements.txt

4️⃣ Configure .env
DATABASE_URL=mysql+pymysql://user:password@localhost/zerophish
JWT_SECRET=your_secret_key

SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your_email@gmail.com
SMTP_PASSWORD=your_password
SMTP_FROM_EMAIL=your_email@gmail.com

BASE_URL=https://your-deployed-domain.com

▶️ Run the App
Backend
python run.py

UI

Open:

http://localhost:8000

🔍 Email Tracking Mechanics
1. Open Tracking (Pixel)

Injected code:

<img src="BASE_URL/track/open/{recipient_id}" width="1" height="1" style="display:none;">


When the email is viewed → server logs the open.

2. Click Tracking
BASE_URL/track/click/{recipient_id}?redirect=REAL_URL


Logged → then user is redirected to the original link.

💰 Business Model (Hackathon Version)
Tier	Price	Employees
Starter	30 AZN / month	Up to 25
Pro	60 AZN / month	Up to 100
Business	119 AZN / month	100+
🧭 Roadmap — Product Milestones
M1 — MVP Completed (Today)

✔️ Tracking system
✔️ AI phishing generator
✔️ Campaign engine
✔️ Admin dashboard

M2 — First Pilot Companies (1–3 SMEs)

Security evaluation

Collect training + real data

Improve email templates

M3 — Integrations

Office365

Gmail Workspace

Admin roles

PDF reporting

M4 — Scale

40–80 paying customers

API expansion

Multi-workspace support

Automated awareness training system

🎯 Why ZeroPhish?

90% of cyber attacks begin with phishing

SMEs lack cybersecurity training

ZeroPhish provides an affordable, automated, and data-driven training solution

Helps companies comply with mandatory security-awareness standards

👥 Team

ZeroPhish is built with passion and security-centric thinking, designed to help organizations stay ahead of attackers — one click at a time.