# 🚀 Enterprise-Grade FastAPI Backend & DevOps Pipeline

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
[![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)](https://www.docker.com/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)
[![AWS](https://img.shields.io/badge/AWS-%23FF9900.svg?style=for-the-badge&logo=amazon-aws&logoColor=white)](https://aws.amazon.com/)
[![GitHub Actions](https://img.shields.io/badge/github%20actions-%232671E5.svg?style=for-the-badge&logo=githubactions&logoColor=white)](https://github.com/features/actions)

This repository demonstrates the development of a production-ready **FastAPI** application. The project covers a complete software lifecycle: from local environment setup with **Poetry** and **Docker** to automated **CI/CD** pipelines and cloud deployment on **AWS (EC2)** with full **Prometheus/Grafana** monitoring.

---

## 🛠 Tech Stack

*   **Language:** Python 3.11+
*   **Framework:** FastAPI (Asynchronous)
*   **Package Manager:** Poetry
*   **Database:** PostgreSQL (Async SQLAlchemy + Alembic migrations)
*   **Security:** JWT, Salted Password Hashing, HTTP-only Cookies
*   **Testing:** Pytest
*   **Monitoring:** Prometheus, Grafana, cAdvisor, Node Exporter
*   **Infrastructure:** Docker Compose, AWS EC2, GitHub Actions

---

## 📈 Development Stages (Laboratory Milestones)

### 📂 Phase 1: Environment & Architecture
*   **Lab 1:** Project initialization with **Poetry**. Multi-branch Git workflow (`prod` and `dev`).
*   **Lab 2:** Multi-container orchestration via **Docker Compose**. Configured hot-reload and volume mounting for live development.
*   **Lab 3:** Scalable directory structure with **APIRouters**. Implemented **Pydantic** schemas for robust data validation.

### 💾 Phase 2: Data & Persistence
*   **Lab 4:** Integrated **PostgreSQL**. Managed complex relational schemas (One-to-Many, One-to-One) across 5+ models. Asynchronous database operations and **Alembic** for migration control.
*   **Lab 5:** Secure Authentication. Implemented **JWT** logic with salted passwords and secure cookie handling.

### 🧪 Phase 3: Quality & Reliability
*   **Lab 6:** Test-Driven Development. Automated unit/integration testing using **Pytest** with a completely isolated PostgreSQL test database.

### 📊 Phase 4: Observability & Cloud Ops
*   **Lab 7:** Full-stack monitoring. Deployed **Prometheus** and **Grafana**. Implemented custom business metrics (e.g., total purchase value) and system-level tracking (CPU, RAM, Container health).
*   **Lab 8:** **CI/CD & Cloud Deployment**. Automated the deployment lifecycle using **GitHub Actions**. Upon push to production, the pipeline runs tests and deploys the stack to an **AWS EC2** instance via SSH.

---

## 🐳 Infrastructure & Monitoring
The project utilizes a 7-container stack for maximum observability:
1.  **FastAPI App** (REST API)
2.  **PostgreSQL** (Primary DB)
3.  **Prometheus** (Metrics collection)
4.  **Grafana** (Data visualization)
5.  **cAdvisor** (Container resource monitoring)
6.  **Node Exporter** (Host machine monitoring)
7.  **Postgres Exporter** (Database health metrics)

---

## 🚀 Deployment Instructions

### Local Development
1.  Install dependencies: `poetry install`
2.  Setup environment variables in `.env`.
3.  Launch containers: `docker compose up -d --build`
4.  Visit API Docs: `http://localhost:8000/docs`

### CI/CD Workflow
The pipeline is automated via GitHub Actions:
*   **Test:** Triggers on pull requests to ensure code quality.
*   **Deploy:** Triggers on push to `prod`. Connects to the AWS instance, pulls latest code, and restarts services.

---
**Developed by:** [Maksym](https://github.com/your-username-here)  
*3rd Year Computer Engineering Student*