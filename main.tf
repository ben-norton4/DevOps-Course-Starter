terraform {
    required_providers {
        azurerm = {
            source = "hashicorp/azurerm"
            version = ">= 2.49"
        }
    }

    backend "azurerm" {
        resource_group_name  = "Zurich1_BenNorton_ProjectExercise"
        storage_account_name = "tfstateyvb9r"
        container_name       = "tfstate"
        key                  = "terraform.tfstate"
    }
}

provider "azurerm" {
    features {}
}

data "azurerm_resource_group" "main" {
    name = "Zurich1_BenNorton_ProjectExercise"
}

resource "azurerm_app_service_plan" "main" {
    name                = "${var.prefix}-terraformed-asp"
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    kind                = "Linux"
    reserved            = true
    sku {
        tier = "Basic"
        size = "B1"
    }
}

resource "azurerm_app_service" "main" {
    name                = "${var.prefix}-app-service-terraformed"
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    app_service_plan_id = azurerm_app_service_plan.main.id
    site_config {
        app_command_line = ""
        linux_fx_version = "DOCKER|bennorton/todo-app-production:latest"
    }
    app_settings = {
        "CLIENT_ID" = var.client_id
        "CLIENT_SECRET" = var.client_secret
        "DATABASE_NAME" = var.database_name
        "DOCKER_REGISTRY_SERVER_PASSWORD" = var.docker_registry_server_password 
        "DOCKER_REGISTRY_SERVER_URL" = var.docker_registry_server_url
        "DOCKER_REGISTRY_SERVER_USERNAME" = var.docker_registry_server_username
        "FLASK_APP" = var.flask_app
        "FLASK_ENV" = var.flask_env
        "FLASK_SKIP_DOTENV" = var.flask_skip_dotenv
        "LOGIN_DISABLED" = var.login_disabled
        "OUATHLIB_INSECURE_TRANSPORT" = var.oauthlib_insecure_transport
        "PORT" = var.port
        "SECRET_KEY" = var.secret_key
        "MONGODB_CONNECTION_STRING" = azurerm_cosmosdb_account.main.connection_strings[0]
    }
}

resource "azurerm_cosmosdb_account" "main" {
    name                = "${var.prefix}-cosmos-db-account-terraformed"
    location            = data.azurerm_resource_group.main.location
    resource_group_name = data.azurerm_resource_group.main.name
    offer_type          = "Standard"
    kind                = "MongoDB"

    enable_automatic_failover = true

    capabilities {
        name = "EnableServerless"
    }

    capabilities {
        name = "mongoEnableDocLevelTTL"
    }

    capabilities {
        name = "MongoDBv3.4"
    }

    capabilities {
        name = "EnableMongo"
    }

    consistency_policy {
        consistency_level       = "BoundedStaleness"
        max_interval_in_seconds = 300
        max_staleness_prefix    = 100000
    }

    geo_location {
        location          = data.azurerm_resource_group.main.location
        failover_priority = 0
    }
}

resource "azurerm_cosmosdb_mongo_database" "main" {
    name                = "${var.prefix}-cosmos-db-terraformed"
    resource_group_name = data.azurerm_resource_group.main.name
    account_name        = azurerm_cosmosdb_account.main.name

    lifecycle {
        prevent_destroy = true
    }
}

resource "random_string" "resource_code" {
    length  = 5
    special = false
    upper   = false
}

resource "azurerm_storage_account" "main" {
    name                     = "tfstate${random_string.resource_code.result}"
    resource_group_name      = data.azurerm_resource_group.main.name
    location                 = data.azurerm_resource_group.main.location
    account_tier             = "Standard"
    account_replication_type = "LRS"

    tags = {
        environment = "staging"
    }
}

resource "azurerm_storage_container" "main" {
    name                  = "tfstate"
    storage_account_name  = azurerm_storage_account.main.name
    container_access_type = "blob"
}
