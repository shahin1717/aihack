🔥 ZeroPhish – AI-Powered Phishing Simulation Platform
📌 SMTP Integration
✉️ Email Sending Methods

ZeroPhish can send phishing simulations using either real corporate email accounts or sandbox SMTP servers.

Supported options:

Gmail SMTP

Workplace / Company SMTP

Custom SMTP server configuration

Local test SMTP

Emails include:

AI-generated subject

AI-generated body content

Tracking pixel

Click-tracking link

Fully logged events (opened, clicked, failed, etc.)

🧱 Backend Tech Stack
🔥 Core Backend

FastAPI

Python

SQLAlchemy ORM

MySQL / PostgreSQL

JWT Authentication

SMTP (email sending)

AI Email Generator (OpenAI / Gemini)

🛰 Tracking Endpoints

GET /track/open/{recipient_id} – open tracking pixel

GET /track/click/{recipient_id} – click redirect logger

🎨 Frontend

HTML

CSS

JavaScript

Fully responsive admin dashboard

Employee manager, campaign creator, logs viewer

🏗 Example Architecture Diagram (like screenshot style)
                   ┌───────────────────────┐
                   │    GitHub Repository  │
                   └───────────┬───────────┘
                               │
                               ▼
                   ┌───────────────────────┐
                   │ GitHub Actions CI/CD  │
                   │ - run tests           │
                   │ - build backend       │
                   │ - deploy              │
                   └───────────┬───────────┘
                               │
                               ▼
                   ┌───────────────────────┐
                   │   Render Deployment   │
                   │ - auto start server   │
                   │ - env variables       │
                   └───────────┬───────────┘
                               ▼

       ┌───────────────────────────────────────────────────┐
       │                 ZeroPhish Platform                │
       │                                                   │
       │  ┌──────────────────────────────┐  ┌────────────┐ │
       │  │         FastAPI API          │  │   Frontend │ │
       │  │ - employees, departments     │  │ - HTML/CSS │ │
       │  │ - auth (JWT)                 │  │ - JS UI    │ │
       │  │ - campaigns, tracking        │  └────────────┘ │
       │  └──────────────────────────────┘                 │
       │                                                   │
       │  ┌──────────────────────────────┐                 │
       │  │        SMTP Server           │                 │
       │  │ - Gmail / Workplace / custom │                 │
       │  │ - sends tracked emails       │                 │
       │  └──────────────────────────────┘                 │
       │                                                   │
       │  ┌──────────────────────────────┐                 │
       │  │         Database             │                 │
       │  │ - employees                  │                 │
       │  │ - campaigns & logs           │                 │
       │  │ - open/click events          │                 │
       │  └──────────────────────────────┘                 │
       └───────────────────────────────────────────────────┘
