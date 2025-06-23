# Variables for the EMR Notebook IAM role configuration

variable "role_name" {
  description = "Name of the IAM role for EMR Notebook"
  type        = string
  default     = "SHC-EMR-NOTEBOOK-ROLE"
}

variable "emr_assumed_role_name" {
  description = "Name of the EMR Assumed Role"
  type        = string
  default     = "SHC-EMR-AssumedRole"
}



variable "tags" {
  description = "Tags to apply to the IAM roles"
  type        = map(string)
  default = {
    Name        = "SHC-EMR-ROLES"
    Description = "IAM roles for EMR with various permissions"
    Environment = "production"
    Project     = "EMR-MWAA-Integration"
  }
}