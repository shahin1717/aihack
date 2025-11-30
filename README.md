# 🛡️ ZeroPhish  
**AI-powered phishing simulation & employee security-awareness platform**

ZeroPhish helps companies test, measure, and improve their employees’ resistance to phishing attacks using AI-generated phishing emails, real-time tracking, and security scoring.

---

## 🚀 Features

- **AI-generated phishing emails** (HTML body + subject)
- **Department & employee management**
- **SMTP integration**  
  - Gmail  
  - Workplace  
  - Custom SMTP servers
- **Multi-recipient campaign sending**
- **Open-tracking pixel**
- **Click-tracking with redirect**
- **Awareness scoring system**
- **Secure JWT authentication**
- **FastAPI backend + responsive JS frontend**

---

## 🛠 Tech Stack

### 🔥 Backend
- **FastAPI**, **Python**
- **SQLAlchemy ORM**
- **MySQL / PostgreSQL**
- **JWT Authentication**
- **SMTP email sending**
- **OpenAI / Google Gemini AI**

### 🎨 Frontend
- **HTML / CSS / JavaScript**
- Custom responsive admin interface

---

## 🏗️ Architecture

```
┌─────────────────┐     ┌────────────────────┐     ┌──────────────────┐
│   GitHub Repo   │───▶ │ GitHub Actions CI  │───▶ │ Render Deployment │
└─────────────────┘     └────────────────────┘     └──────────────────┘
                              │                             │
                              ▼                             ▼

                    ┌─────────────────────┐    ┌─────────────────────┐
                    │     FastAPI API     │    │     Frontend UI      │
                    │  Auth / Employees   │    │  Dashboard / Campaign │
                    │  Departments        │    │  Tracking Pages       │
                    │  Campaigns/Tracking │    └─────────────────────┘
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │      SMTP Server     │
                    │ Gmail / Workplace    │
                    │ Custom SMTP          │
                    └─────────────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │    Database (SQL)   │
                    │ Employees           │
                    │ Campaigns           │
                    │ Recipients          │
                    │ Tracking Events     │
                    └─────────────────────┘
```

---

## 📦 Installation

### 1. Clone the repository
```bash
git clone https://github.com/your-username/zerophish.git
cd zerophish
```

### 2. Create a virtual environment
```bash
python -m venv .venv
source .venv/bin/activate       # macOS / Linux
.venv\Scripts\Activate.ps1      # Windows
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the server
```bash
python run.py
```

Open the dashboard:  
👉 **http://127.0.0.1:8000/employees.html**

---

## ⚙️ Environment Variables

Create a `.env` file:

```
SECRET_KEY=your-secret-key
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-email-password
DB_URL=mysql+pymysql://user:password@localhost/zerophish
OPENAI_API_KEY=your-key
```

---

## ✉️ Example Email With Tracking

```html
<p>Dear Employee,</p>
<p>Suspicious activity detected. Please verify your account.</p>

<a href="https://yourdomain.com/track/click/42?redirect=https://google.com">
  Verify Your Account
</a>

<img src="https://yourdomain.com/track/open/42" width="1" height="1" />
```

---

## 🔌 Tracking Endpoints

| Endpoint | Description |
|---------|-------------|
| `GET /track/open/{id}` | Logs the *open* event |
| `GET /track/click/{id}?redirect=URL` | Logs click event & redirects user |

---

## 📁 Project Structure

```
zerophish/
├── app/
│   ├── routers/
│   ├── database/
│   ├── static/
│   ├── templates/
│   ├── email_sender.py
│   └── main.py
├── requirements.txt
├── run.py
└── README.md
```

---

## 📊 Dashboard Features

- Campaign analytics  
- Open rate / click rate  
- Per-employee and per-department scores  
- Tracking logs  
- AI email generator  
- Admin authentication  

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch  
3. Commit changes  
4. Push your branch  
5. Open a Pull Request  

---

## 📄 License

MIT License  
https://choosealicense.com/licenses/mit/

