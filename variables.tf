# Variables for AWS Secrets Manager configuration

variable "environment" {
  description = "Environment name (e.g., production, staging, development)"
  type        = string
  default     = "production"
}

variable "project_name" {
  description = "Name of the project"
  type        = string
  default     = "snowflake_demo"
}

variable "recovery_window_in_days" {
  description = "Number of days that AWS Secrets Manager waits before it can delete the secret"
  type        = number
  default     = 30

  validation {
    condition     = var.recovery_window_in_days >= 0 && var.recovery_window_in_days <= 30
    error_message = "Recovery window must be between 0 and 30 days."
  }
}

variable "enable_automatic_rotation" {
  description = "Whether to enable automatic rotation for secrets"
  type        = bool
  default     = false
}

# KMS Key Variables
variable "kms_deletion_window_in_days" {
  description = "Number of days after which KMS key is deleted after destruction"
  type        = number
  default     = 30

  validation {
    condition     = var.kms_deletion_window_in_days >= 7 && var.kms_deletion_window_in_days <= 30
    error_message = "KMS deletion window must be between 7 and 30 days."
  }
}

variable "enable_kms_key_rotation" {
  description = "Whether to enable automatic rotation for KMS keys"
  type        = bool
  default     = true
}

variable "common_tags" {
  description = "Common tags to apply to all secrets"
  type        = map(string)
  default = {
    Project   = "snowflake_demo"
    ManagedBy = "terraform"
    Owner     = "data-platform-team"
  }
}

# Environment-specific configurations
variable "environments" {
  description = "Environment-specific configurations"
  type = map(object({
    recovery_window = number
    tags            = map(string)
  }))
  default = {
    production = {
      recovery_window = 30
      tags = {
        Environment = "production"
        Criticality = "high"
      }
    }
    staging = {
      recovery_window = 7
      tags = {
        Environment = "staging"
        Criticality = "medium"
      }
    }
    development = {
      recovery_window = 0
      tags = {
        Environment = "development"
        Criticality = "low"
      }
    }
  }
}