# 📦 Backup Center (Woking in progress)

Distributed backend system for automated backup of network devices (OLT, routers, switches) using asynchronous processing.

---

## 🧠 Overview

**Backup Center** is designed to automate the collection of network device configurations via SSH in a scalable and reliable way.

The system uses an API to receive requests, a message queue to decouple processing, and workers to execute backup tasks asynchronously.

---

## 🏗️ Architecture

```text
Client (NOC / Admin)
        ↓
      Flask
        ↓
   Redis (Queue)
        ↓
   Celery Workers
        ↓
 Network Devices (SSH)
        ↓
 Storage (Filesystem / S3)
```

---

## 📁 Project Structure

```bash
backup-center/
│
├── app/
│   ├── api/                # API routes (Flask)
│   ├── core/               # Core configs (Celery, settings)
│   ├── services/           # Business logic (SSH, backup, storage)
│   ├── workers/            # Async tasks (Celery)
│   └── main.py             # Application entry point
│
├── docker-compose.yml
├── requirements.txt
└── .env.example
```

---

## ⚙️ Core Components

### API Layer (Flask)
- Receives requests to trigger backups
- Validates input
- Sends tasks to the queue

### Queue (Redis)
- Decouples API from execution
- Enables asynchronous processing
- Handles task distribution

### Workers (Celery)
- Execute backup jobs
- Connect to devices via SSH
- Process and store configurations

### Scheduler (Celery Beat)
- Automates periodic backups
- Supports cron-like scheduling

---

## 🔄 Execution Flow

```text
1. Request received via API or scheduler
2. Task is sent to Redis queue
3. Worker consumes task
4. SSH connection is established
5. Commands are executed on device
6. Configuration is retrieved
7. Output is processed and saved
8. Optional notification is triggered
```

---

## 🔐 Environment Configuration

Create a `.env` file:

```env
REDIS_URL=redis://redis:6379/0
BACKUP_PATH=/data/backups
```

---

## ▶️ Running with Docker

```bash
docker-compose up --build
```

---

## 🐳 Services

- **api** → Flask application
- **worker** → Celery worker (task execution)
- **beat** → Celery scheduler
- **redis** → message broker

---

## 📁 Output Structure

```bash
backups/
├── device-1/
│   └── 2026-04-27.txt
├── device-2/
│   └── 2026-04-27.txt
```

---

## 🛡️ Security

- No hardcoded credentials
- Environment-based configuration
- Recommended:
  - Secrets manager
  - Encrypted storage
  - Access control (JWT)

---

## 📈 Scalability

- Stateless API
- Horizontal worker scaling
- Queue-based load distribution
- Ready for container orchestration (Docker/Kubernetes)

---

## 🔍 Observability (Recommended)

- Structured logging
- Metrics (Prometheus)
- Tracing (OpenTelemetry)

---

## 🚀 Future Improvements

- Multi-vendor support (Huawei, ZTE, Mikrotik)
- REST API authentication (JWT)
- Web dashboard
- Database integration (PostgreSQL)
- Backup versioning & diff
- Object storage (S3 / MinIO)

---

## 📄 License

MIT
