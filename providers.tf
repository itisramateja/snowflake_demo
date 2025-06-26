# Terraform configuration
terraform {
  required_version = ">= 1.0"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }

  # Uncomment and configure backend as needed
  # backend "s3" {
  #   bucket = "your-terraform-state-bucket"
  #   key    = "secrets-manager/terraform.tfstate"
  #   region = "us-east-1"
  # }
}

# AWS Provider configuration
provider "aws" {
  region = var.aws_region

  default_tags {
    tags = var.common_tags
  }
}

# AWS region variable
variable "aws_region" {
  description = "AWS region for resources"
  type        = string
  default     = "us-east-1"
}