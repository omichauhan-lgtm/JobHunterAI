# 16 - Cloud Deployment & DevOps Guide

This document defines the architecture and deployment steps to host **JobHunterAI** as a persistent, cloud-native Career Intelligence Platform (V8).

---

## 🏗️ Cloud Architecture

The platform is designed to run in a containerized environment (Docker & Docker Compose), allowing deployment to any Virtual Private Server (VPS), cloud VM (AWS EC2, DigitalOcean, Linode), or container service (Render, Fly.io).

```
Host Server (Cron Daemon)
       │
       ▼ (Daily at 08:00)
┌──────────────┐          ┌──────────────┐
│  compose     │          │  compose     │
│  worker      │          │  web UI      │
│  (Container) │          │  (Container) │
└──────┬───────┘          └──────┬───────┘
       │                         │
       └───────────┬─────────────┘
                   ▼
         ┌───────────────────┐
         │ Persistent Volume │
         │   (candidate.db)  │
         └───────────────────┘
```

---

## 🛠️ Step-by-Step Deployment

### 1. Prerequisites
Ensure the target server has **Docker** and **Docker Compose** installed:
```bash
sudo apt-get update
sudo apt-get install docker-ce docker-ce-cli containerd.io docker-compose-plugin
```

### 2. Environment Setup
Clone the repository to the server and create a production `.env` file:
```ini
GEMINI_API_KEY=your_gemini_api_key
OPENAI_API_KEY=your_openai_api_key
JOB_APPLY_THRESHOLD=70.0
DEFAULT_RESUME_TEMPLATE=backend.tex

# Email Notification configurations
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
RECIPIENT_EMAIL=your_delivery_email@gmail.com
```

### 3. Build & Launch Web Service
Build the container images and launch the Streamlit frontend service:
```bash
docker compose up -d web
```
The web dashboard is now exposed and active on port `8501`.

---

## ⏰ Background Loop Scheduling

To execute the daily discovery and briefing loop autonomously without keeping your personal computer turned on:
1. Open the host server's crontab:
   ```bash
   crontab -e
   ```
2. Append a daily entry to run the worker container at 08:00 every morning:
   ```text
   0 8 * * * cd /path/to/JobHunterAI && docker compose run --rm worker >> /var/log/jobhunter_worker.log 2>&1
   ```

This command launches the worker container, executes `main.py --daily-loop` (updating the database volume and sending the daily email briefing), and automatically destroys the temporary container (`--rm`), preserving resources on your cloud node.
