variable "docker_host" {
  description = "Docker host URI. Use npipe on Windows or unix socket on Linux/macOS."
  type        = string
  default     = "npipe:////./pipe/docker_engine"
}

variable "postgres_user" {
  description = "PostgreSQL username"
  type        = string
  default     = "postgres"
}

variable "postgres_password" {
  description = "PostgreSQL password"
  type        = string
  default     = "postgres"
}

variable "postgres_db" {
  description = "PostgreSQL database name"
  type        = string
  default     = "tradingbot"
}
