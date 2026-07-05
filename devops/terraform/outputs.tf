output "backend_url" {
  description = "URL for the backend API"
  value       = "http://localhost:8000"
}

output "frontend_url" {
  description = "URL for the frontend UI"
  value       = "http://localhost:5173"
}

output "postgres_container_id" {
  description = "Docker container ID for PostgreSQL"
  value       = docker_container.db.id
}

output "redis_container_id" {
  description = "Docker container ID for Redis"
  value       = docker_container.redis.id
}
