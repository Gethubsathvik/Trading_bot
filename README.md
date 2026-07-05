# Tradingbot

## Project Overview

Tradingbot is a starter trading platform that combines quick local development with an infrastructure-as-code deployment model.

The current project includes:
- A FastAPI backend for APIs, WebSocket events, and trade orchestration
- A React + Vite frontend for user interaction and dashboard rendering
- A Flutter mobile scaffold in `mobile/` for future mobile client support
- Docker Compose for local container orchestration
- Terraform for infrastructure-as-code and repeatable Docker deployments

This repository is designed as a foundation for a trading system that can evolve into a complete production platform.

## What This Project Does Today

Today, the repository provides:
- Backend service scaffolding with health checks and a WebSocket stub
- Frontend starter UI with React, Vite, and TypeScript
- Local development support using Docker Compose
- Infrastructure automation using Terraform for local Docker containers

It is not yet a fully functioning trading system. The current code is a strong base for building market data pipelines, trading strategies, order execution, and portfolio dashboards.

## Architecture

### Component layout

- `backend/`
  - FastAPI service in `backend/src/main.py`
  - Serves REST endpoints and a WebSocket endpoint at `/ws/market`
  - Intended to connect to PostgreSQL, Redis, and exchange APIs
  - Can be extended with background workers for strategy execution

- `frontend/`
  - React application with TypeScript, Vite, and static build support
  - Entry point is `frontend/src/main.tsx`
  - Main UI component is `frontend/src/App.tsx`
  - Designed to evolve into trading dashboards, order forms, and market charts

- `devops/`
  - `docker-compose.yml` for running backend, Redis, and PostgreSQL locally
  - `terraform/` for infrastructure-as-code, building the same stack with Terraform

- `mobile/`
  - Flutter scaffold in `mobile/lib/main.dart`
  - Provides a mobile-native entry point for future app development

### System flow

The intended flow for a production-ready Tradingbot is:
1. Frontend requests market data and trading status from the backend.
2. Backend fetches or streams market data from exchange APIs.
3. Backend stores state in PostgreSQL and caches active session data in Redis.
4. WebSocket delivers live updates to the frontend.
5. Orders and signals are processed by backend services and executed via exchange integrations.
6. Optional Celery workers handle asynchronous tasks such as trade execution, data aggregation, and notifications.

## Folder Structure

- `backend/` — backend API and service logic
- `frontend/` — web user interface and static frontend code
- `devops/` — deployment and infrastructure definitions
- `devops/terraform/` — Terraform files for local Docker deployment
- `mobile/` — Flutter mobile app scaffold

## Technology Stack

### Languages Used

This project includes code written in several languages:
- Python — backend service and API logic
- TypeScript — frontend application and Vite configuration
- JavaScript — build scripts, linting, and browser assets
- Dart — mobile application scaffold with Flutter
- HCL (HashiCorp Configuration Language) — Terraform infrastructure code
- YAML — Docker Compose and configuration files
- Shell / PowerShell — local run commands and deployment scripts

### Backend

The backend uses Python and the following libraries:
- `fastapi` — high-performance ASGI API framework
- `uvicorn` — ASGI server for running FastAPI
- `sqlalchemy` — ORM for relational database access
- `alembic` — database schema migrations
- `psycopg2-binary` — PostgreSQL database driver
- `redis` — Redis client
- `celery` — task queue for background jobs
- `python-jose[cryptography]` — JWT and token handling
- `passlib[bcrypt]` — secure password hashing
- `python-multipart` — file upload and form parsing
- `pydantic` / `pydantic-settings` — validation and typed settings
- `websockets` — WebSocket support for real-time messaging
- `ccxt` — exchange connectivity for crypto trading
- `pandas`, `numpy`, `ta-lib` — market analytics and indicator computation
- `httpx` — async HTTP client for external APIs
- `pytest` — testing framework

### Frontend

The frontend uses JavaScript and TypeScript libraries:
- `react` / `react-dom` — component-based UI library
- `vite` — fast development server and build tool
- `typescript` — typed JavaScript support
- `@vitejs/plugin-react` — React integration for Vite
- `eslint` + plugins — code quality and style enforcement
- `tailwindcss` — utility-first CSS framework
- `postcss` — CSS transformation and processing

### Infrastructure

The infrastructure supports both container-based local development and infrastructure-as-code:
- `Docker Compose` provides a simple `up/down` workflow for local services
- `Dockerfiles` define how the backend and frontend images are built
- `Terraform` allows the same stack to be managed with code, enabling reproducible deployment and future cloud migration

## Local Deployment

### Backend only

```powershell
cd Tradingbot/backend
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

Open `http://localhost:8000/`

### Frontend only

```powershell
cd Tradingbot/frontend
npm install
npm run dev
```

Open `http://localhost:5173`

### Local Docker Compose

```powershell
cd Tradingbot/devops
docker compose up --build
```

This launches:
- backend on `http://localhost:8000`
- Redis on `localhost:6379`
- PostgreSQL on `localhost:5432`

### Terraform local Docker deployment

```powershell
cd Tradingbot/devops/terraform
terraform init
terraform apply
```

To destroy the environment:

```powershell
terraform destroy
```

## Infrastructure Details

### Docker Compose

`devops/docker-compose.yml` defines:
- backend service built from `backend/Dockerfile`
- PostgreSQL database service
- Redis cache service
- shared network and data volume for persistence

### Terraform

`devops/terraform/` defines:
- Docker provider configuration
- local Docker network creation
- image builds for backend and frontend
- container deployments for PostgreSQL, Redis, backend, and frontend
- outputs for service URLs and container IDs

This makes local infrastructure repeatable and easier to version control.

## Future Enhancements

This repository is a foundation, not a finished product. Key next steps include:
- implement real market data streaming and exchange connectors
- add user authentication, authorization, and account management
- build trading strategies, risk management, and order execution flows
- implement dashboards for balances, positions, and trade history
- add mobile app screens and cross-platform client support
- add observability with logs, metrics, and alerts
- add CI/CD and production deployment automation

## Notes

- The backend currently contains scaffolding and a WebSocket stub rather than production trading logic.
- The frontend is a starter application meant to be extended with real trading UI.
- The mobile app is a placeholder scaffold for future native support.
- This project is useful as a reference architecture for a trading platform using Python, React, Docker, and Terraform.
