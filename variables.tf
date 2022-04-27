variable "prefix" {
    description = "The prefix used for all resources in this environment"
    default     = "dva"
}

variable "location" {
    description = "The Azure location where all resources in this deployment should be created"
    default     = "uksouth"
}

variable "client_id" {
    description = ""
    default     = "7fbc92de3ce4f03de02d"
}

variable "client_secret" {
    description = ""
    sensitive = "true"
}

variable "database_name" {
    description = ""
    default     = "todo_app_database"
}

variable "docker_registry_server_password" {
    description = ""
    sensitive = "true"
}

variable "docker_registry_server_url" {
    description = ""
    default     = "https://index.docker.io"
}

variable "docker_registry_server_username" {
    description = ""
    default     = "bennorton"
}

variable "flask_app" {
    description = ""
    default     = "todo_app/app"
}

variable "flask_env" {
    description = ""
    default     = "production"
}

variable "flask_skip_dotenv" {
    description = ""
    default     = "true"
}

variable "login_disabled" {
    description = ""
    default     = "false"
}

variable "oauthlib_insecure_transport" {
    description = ""
    default     = "1"
}

variable "port" {
    description = ""
    default     = "5000"
}

variable "secret_key" {
    description = ""
    sensitive   =  "true"
}
