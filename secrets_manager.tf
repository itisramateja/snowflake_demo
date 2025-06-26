# AWS Secrets Manager Resources
# This file contains all the secrets used across different environments and services

# Local values for secret configurations
locals {
  # Base tags that will be merged with specific tags
  base_tags = merge(var.common_tags, {
    Environment = var.environment
  })

  # Secret configurations with their metadata
  secrets_config = {
    # API and Service Secrets
    eventcombo = {
      description = "EventCombo service API credentials and configuration"
      tags = {
        Service = "eventcombo"
        Type    = "api-credentials"
      }
    }

    providers_api = {
      description = "API credentials and configuration for external providers"
      tags = {
        Service = "providers"
        Type    = "api-credentials"
      }
    }

    talkdesk = {
      description = "Talkdesk contact center platform API credentials"
      tags = {
        Service = "talkdesk"
        Type    = "api-credentials"
      }
    }

    "xmatters/nonprod/api" = {
      description = "xMatters non-production environment API credentials"
      tags = {
        Environment = "nonprod"
        Service     = "xmatters"
        Type        = "api-credentials"
      }
    }

    mdstaff = {
      description = "MDStaff application database and service credentials"
      tags = {
        Service = "mdstaff"
        Type    = "service-credentials"
      }
    }

    "mdstaff-api" = {
      description = "MDStaff API service credentials and configuration"
      tags = {
        Service = "mdstaff"
        Type    = "api-credentials"
      }
    }

    "mdstaff-client" = {
      description = "MDStaff client application credentials"
      tags = {
        Service = "mdstaff"
        Type    = "client-credentials"
      }
    }

    vizient_risk_api = {
      description = "Vizient Risk API credentials and configuration"
      tags = {
        Service = "vizient"
        Type    = "api-credentials"
      }
    }

    "viz-api-cdb-credentials" = {
      description = "Vizient API CouchDB database credentials"
      tags = {
        Service = "vizient"
        Type    = "database-credentials"
      }
    }

    "viz-api" = {
      description = "Vizient API service credentials and configuration"
      tags = {
        Service = "vizient"
        Type    = "api-credentials"
      }
    }

    contentful = {
      description = "Contentful CMS API credentials and configuration"
      tags = {
        Service = "contentful"
        Type    = "api-credentials"
      }
    }

    "imo-client" = {
      description = "IMO client application credentials"
      tags = {
        Service = "imo"
        Type    = "client-credentials"
      }
    }

    "healthy-places" = {
      description = "Healthy Places application credentials and configuration"
      tags = {
        Service = "healthy-places"
        Type    = "service-credentials"
      }
    }

    # Snowflake and Data Platform Secrets
    "sflk-svcdatahub" = {
      description = "Snowflake service account credentials for DataHub integration"
      tags = {
        Service   = "snowflake"
        Type      = "service-account"
        Component = "datahub"
      }
    }

    "sflk-svc-user" = {
      description = "Snowflake service user credentials"
      tags = {
        Service = "snowflake"
        Type    = "service-account"
      }
    }

    dbt_user = {
      description = "DBT (Data Build Tool) user credentials for data transformations"
      tags = {
        Service = "dbt"
        Type    = "service-account"
      }
    }

    "shc-snowflake" = {
      description = "SHC Snowflake connection credentials"
      tags = {
        Service      = "snowflake"
        Type         = "connection-credentials"
        Organization = "shc"
      }
    }

    # DataHub Secrets
    "prod/datahub_source_secrets" = {
      description = "Production DataHub data source connection secrets"
      tags = {
        Service = "datahub"
        Type    = "source-credentials"
      }
    }

    "prod/datahub/secrets" = {
      description = "Production DataHub application secrets and configuration"
      tags = {
        Service = "datahub"
        Type    = "application-secrets"
      }
    }

    "shc-datahub-prod-opensearch" = {
      description = "SHC DataHub production OpenSearch cluster credentials"
      tags = {
        Service      = "datahub"
        Type         = "database-credentials"
        Component    = "opensearch"
        Organization = "shc"
      }
    }

    # Development and Deployment Secrets
    "prod/lookml-github-deploy-key" = {
      description = "Production LookML GitHub deployment key for automated deployments"
      tags = {
        Service   = "lookml"
        Type      = "deploy-key"
        Component = "github"
      }
    }

    "ecs-task-dev-dbtoncloud/dev/SFLKConn/dbtoncloud" = {
      description = "ECS task development environment DBT Cloud Snowflake connection credentials"
      tags = {
        Environment = "development"
        Service     = "ecs"
        Type        = "task-credentials"
        Component   = "dbt-cloud"
      }
    }

    # AWS and Third-party Service Secrets
    windowsdefender = {
      description = "Windows Defender ATP API credentials and configuration"
      tags = {
        Service = "windows-defender"
        Type    = "api-credentials"
      }
    }

    "aws-s3-fivetran" = {
      description = "AWS S3 credentials for Fivetran data pipeline integration"
      tags = {
        Service   = "fivetran"
        Type      = "aws-credentials"
        Component = "s3"
      }
    }

    "AmazonSageMaker-3f3c404d1fdf49d29b82332c9ea62032" = {
      description = "Amazon SageMaker service credentials and configuration"
      tags = {
        Service = "sagemaker"
        Type    = "service-credentials"
      }
    }
  }
}

# Create all secrets using for_each for better maintainability
resource "aws_secretsmanager_secret" "secrets" {
  for_each = local.secrets_config

  name                    = each.key
  description             = each.value.description
  recovery_window_in_days = var.recovery_window_in_days

  tags = merge(
    local.base_tags,
    each.value.tags
  )
}

# Secret Versions (Optional - uncomment and modify as needed)
# These create empty secret versions that can be populated later

/*
resource "aws_secretsmanager_secret_version" "eventcombo" {
  secret_id = aws_secretsmanager_secret.eventcombo.id
  secret_string = jsonencode({
    api_key = "placeholder"
    api_url = "placeholder"
  })
  
  lifecycle {
    ignore_changes = [secret_string]
  }
}

resource "aws_secretsmanager_secret_version" "providers_api" {
  secret_id = aws_secretsmanager_secret.providers_api.id
  secret_string = jsonencode({
    api_key = "placeholder"
    api_url = "placeholder"
  })
  
  lifecycle {
    ignore_changes = [secret_string]
  }
}

# Add more secret versions as needed...
*/

# Outputs for reference
output "secret_arns" {
  description = "ARNs of all created secrets"
  value = {
    for name, secret in aws_secretsmanager_secret.secrets : name => secret.arn
  }
}

output "secret_names" {
  description = "Names of all created secrets"
  value = [
    for secret in aws_secretsmanager_secret.secrets : secret.name
  ]
}

output "secrets_by_service" {
  description = "Secrets grouped by service"
  value = {
    for name, config in local.secrets_config :
    lookup(config.tags, "Service", "unknown") => name...
  }
}

output "secrets_by_type" {
  description = "Secrets grouped by type"
  value = {
    for name, config in local.secrets_config :
    lookup(config.tags, "Type", "unknown") => name...
  }
}