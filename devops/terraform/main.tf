terraform {
  required_version = ">= 1.5.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 2.20.0"
    }
  }
}

provider "docker" {
  host = var.docker_host
}

resource "docker_network" "tradingbot" {
  name = "tradingbot_network"
}

resource "docker_image" "postgres" {
  name = "postgres:15-alpine"
}

resource "docker_image" "redis" {
  name = "redis:alpine"
}

resource "docker_image" "backend" {
  name = "tradingbot-backend:latest"
  build {
    context    = "../../backend"
    dockerfile = "Dockerfile"
  }
}

resource "docker_image" "frontend" {
  name = "tradingbot-frontend:latest"
  build {
    context    = "../../frontend"
    dockerfile = "Dockerfile"
  }
}

resource "docker_container" "db" {
  name  = "tradingbot-db"
  image = docker_image.postgres.name
  restart = "unless-stopped"
  networks_advanced {
    name = docker_network.tradingbot.name
  }
  env = [
    "POSTGRES_USER=${var.postgres_user}",
    "POSTGRES_PASSWORD=${var.postgres_password}",
    "POSTGRES_DB=${var.postgres_db}"
  ]
  ports {
    internal = 5432
    external = 5432
  }
}

resource "docker_container" "redis" {
  name  = "tradingbot-redis"
  image = docker_image.redis.name
  restart = "unless-stopped"
  networks_advanced {
    name = docker_network.tradingbot.name
  }
  ports {
    internal = 6379
    external = 6379
  }
}

resource "docker_container" "backend" {
  name  = "tradingbot-backend"
  image = docker_image.backend.name
  restart = "unless-stopped"
  networks_advanced {
    name = docker_network.tradingbot.name
  }
  ports {
    internal = 8000
    external = 8000
  }
  env = [
    "DATABASE_URL=postgresql://${var.postgres_user}:${var.postgres_password}@${docker_container.db.name}:5432/${var.postgres_db}",
    "REDIS_URL=redis://redis:6379/0"
  ]
  depends_on = [
    docker_container.db,
    docker_container.redis
  ]
}

resource "docker_container" "frontend" {
  name  = "tradingbot-frontend"
  image = docker_image.frontend.name
  restart = "unless-stopped"
  networks_advanced {
    name = docker_network.tradingbot.name
  }
  ports {
    internal = 80
    external = 5173
  }
  depends_on = [
    docker_container.backend
  ]
}
