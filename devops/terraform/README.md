# Terraform Local Docker Deployment

This folder contains Terraform configuration for local Docker-based deployment of the Tradingbot stack.

## Prerequisites

- Docker installed and running
- Terraform installed (recommended `>= 1.5.0`)

## What it deploys

- `tradingbot-db` PostgreSQL container
- `tradingbot-redis` Redis container
- `tradingbot-backend` backend service container
- `tradingbot-frontend` frontend service container
- `tradingbot_network` Docker network for service connectivity

## Usage

```powershell
cd Tradingbot/devops/terraform
terraform init
terraform apply
```

The frontend will be available at `http://localhost:5173` and the backend at `http://localhost:8000`.

## Cleanup

```powershell
terraform destroy
```

## Notes

- The backend image is built from `../../backend`
- The frontend image is built from `../../frontend`
- The configuration uses the Docker provider and is intended for local development
