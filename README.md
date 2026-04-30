# 🧪 Development Evidence & Technical Documentation

This branch serves as a workspace for development and contains all technical evidence required for laboratory evaluations. Below is a structured gallery of screenshots, logs, and command sequences documenting the project's evolution.

---

## 📂 Laboratory Work Gallery

### 🔹 Lab 1: Environment Setup
*   **Git History:** [Link to log file or screenshot of git logs]
*   **Description:** Initialization of the Poetry project, branch management (`prod`/`dev`), and `.gitignore` configuration.

### 🔹 Lab 2: Containerization
*   **Running Containers:** Screenshots showing active FastAPI and PostgreSQL containers.
*   **Command History:** Text file containing the exact sequence of Docker commands used.
*   **Environment:** List of installed libraries inside the container (`pip list` / `poetry show`).

### 🔹 Lab 3: API Architecture & Routing
*   **Postman Testing:** Screenshots of successful `GET`, `POST`, `PUT`, and `DELETE` requests.
*   **Validation:** Evidence of Pydantic schema validation for user models.

### 🔹 Lab 4: Database & Migrations
*   **DB Schema:** Screenshots of the PostgreSQL database structure showing 5+ models and relationships.
*   **Data Entries:** Proof of initial data populated in tables (categories, products, etc.) via SQLAlchemy.
*   **Alembic:** Evidence of successful migration history.

### 🔹 Lab 5: Security & Auth
*   **JWT Implementation:** Evidence of registration and authentication flow.
*   **Secure Access:** Screenshots of "Protected" routes requiring a valid JWT token/cookie.

### 🔹 Lab 6: Quality Assurance
*   **Pytest Results:** Full console output showing all tests passing on an isolated test database.

### 🔹 Lab 7: Observability & Monitoring
*   **Grafana Dashboards:** Screenshots of:
    *   System metrics (CPU/RAM usage).
    *   Docker container health (cAdvisor).
    *   PostgreSQL status.
    *   Custom business metrics (e.g., Total Purchase Value).
*   **Prometheus:** Verification of the metrics scraping targets.

### 🔹 Lab 8: Cloud Infrastructure & CI/CD
*   **AWS Console:** Proof of running EC2 instance (`t3.micro`) with expanded 20GB storage.
*   **GitHub Actions:** Screenshots of successful pipeline runs (Test -> Build -> Deploy).
*   **Production URL:** Final evidence of the API reachable via AWS Public IP.

---

## 🛠 Useful Dev Commands

**Check container status:**
```bash
docker ps