# AWS KMS Keys Configuration
# This file contains all the KMS keys used across different environments and services

# Local values for KMS key configurations
locals {
  # KMS key configurations with their metadata
  kms_keys_config = {
    # MWAA (Managed Workflows for Apache Airflow) Keys
    "shc-dts-nonprod-mwaa" = {
      description = "KMS key for SHC DTS non-production MWAA environment encryption"
      tags = {
        Environment  = "nonprod"
        Service      = "mwaa"
        Organization = "shc"
        Team         = "dts"
        Purpose      = "airflow-encryption"
      }
    }

    "shc-dts-test-mwaa" = {
      description = "KMS key for SHC DTS test MWAA environment encryption"
      tags = {
        Environment  = "test"
        Service      = "mwaa"
        Organization = "shc"
        Team         = "dts"
        Purpose      = "airflow-encryption"
      }
    }

    "shc-dts-prod-mwaa" = {
      description = "KMS key for SHC DTS production MWAA environment encryption"
      tags = {
        Environment  = "production"
        Service      = "mwaa"
        Organization = "shc"
        Team         = "dts"
        Purpose      = "airflow-encryption"
      }
    }

    # EKS Cluster Keys
    "cmk-eks-tawseksprod-cluster" = {
      description = "Customer Managed Key for EKS production cluster encryption"
      tags = {
        Environment = "production"
        Service     = "eks"
        Cluster     = "tawseksprod"
        Purpose     = "cluster-encryption"
      }
    }

    "cmk-eks-tawseksdev-cluster" = {
      description = "Customer Managed Key for EKS development cluster encryption"
      tags = {
        Environment = "development"
        Service     = "eks"
        Cluster     = "tawseksdev"
        Purpose     = "cluster-encryption"
      }
    }

    "cmk-eks-tawseksqa-cluster" = {
      description = "Customer Managed Key for EKS QA cluster encryption"
      tags = {
        Environment = "qa"
        Service     = "eks"
        Cluster     = "tawseksqa"
        Purpose     = "cluster-encryption"
      }
    }

    # SageMaker Key
    "shc-ea-sagemaker-key100" = {
      description = "KMS key for SHC EA SageMaker service encryption"
      tags = {
        Environment  = "production"
        Service      = "sagemaker"
        Organization = "shc"
        Team         = "ea"
        Purpose      = "ml-encryption"
        KeyVersion   = "100"
      }
    }
  }

  # KMS key policy for different services
  mwaa_key_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow MWAA Service"
        Effect = "Allow"
        Principal = {
          Service = "airflow.amazonaws.com"
        }
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey",
          "kms:CreateGrant"
        ]
        Resource = "*"
        Condition = {
          StringEquals = {
            "kms:ViaService" = "s3.${var.aws_region}.amazonaws.com"
          }
        }
      }
    ]
  })

  eks_key_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow EKS Service"
        Effect = "Allow"
        Principal = {
          Service = "eks.amazonaws.com"
        }
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey",
          "kms:CreateGrant"
        ]
        Resource = "*"
      }
    ]
  })

  sagemaker_key_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "Enable IAM User Permissions"
        Effect = "Allow"
        Principal = {
          AWS = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:root"
        }
        Action   = "kms:*"
        Resource = "*"
      },
      {
        Sid    = "Allow SageMaker Service"
        Effect = "Allow"
        Principal = {
          Service = "sagemaker.amazonaws.com"
        }
        Action = [
          "kms:Decrypt",
          "kms:GenerateDataKey",
          "kms:CreateGrant",
          "kms:ReEncrypt*",
          "kms:DescribeKey"
        ]
        Resource = "*"
      }
    ]
  })
}

# Data source to get current AWS account ID
data "aws_caller_identity" "current" {}

# Create all KMS keys using for_each for better maintainability
resource "aws_kms_key" "keys" {
  for_each = local.kms_keys_config

  description              = each.value.description
  key_usage                = "ENCRYPT_DECRYPT"
  customer_master_key_spec = "SYMMETRIC_DEFAULT"
  deletion_window_in_days  = var.kms_deletion_window_in_days
  enable_key_rotation      = var.enable_kms_key_rotation

  # Set policy based on service type
  policy = contains(keys(each.value.tags), "Service") ? (
    each.value.tags.Service == "mwaa" ? local.mwaa_key_policy :
    each.value.tags.Service == "eks" ? local.eks_key_policy :
    each.value.tags.Service == "sagemaker" ? local.sagemaker_key_policy :
    null
  ) : null

  tags = merge(
    local.base_tags,
    each.value.tags,
    {
      Name = each.key
    }
  )
}

# Create KMS aliases for easier identification
resource "aws_kms_alias" "key_aliases" {
  for_each = local.kms_keys_config

  name          = "alias/${each.key}"
  target_key_id = aws_kms_key.keys[each.key].key_id
}

# KMS Key Grants (Optional - uncomment and modify as needed)
# These provide specific permissions to services or roles

/*
# Example: Grant for MWAA service role
resource "aws_kms_grant" "mwaa_grants" {
  for_each = {
    for name, config in local.kms_keys_config : name => config
    if lookup(config.tags, "Service", "") == "mwaa"
  }
  
  name              = "${each.key}-mwaa-grant"
  key_id            = aws_kms_key.keys[each.key].key_id
  grantee_principal = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/service-role/AmazonMWAA-${each.key}-ExecutionRole"
  
  operations = [
    "Decrypt",
    "GenerateDataKey",
    "CreateGrant",
    "RetireGrant"
  ]
}

# Example: Grant for EKS cluster service role
resource "aws_kms_grant" "eks_grants" {
  for_each = {
    for name, config in local.kms_keys_config : name => config
    if lookup(config.tags, "Service", "") == "eks"
  }
  
  name              = "${each.key}-eks-grant"
  key_id            = aws_kms_key.keys[each.key].key_id
  grantee_principal = "arn:aws:iam::${data.aws_caller_identity.current.account_id}:role/${lookup(each.value.tags, "Cluster", "unknown")}-cluster-ServiceRole"
  
  operations = [
    "Decrypt",
    "GenerateDataKey",
    "CreateGrant",
    "RetireGrant"
  ]
}
*/