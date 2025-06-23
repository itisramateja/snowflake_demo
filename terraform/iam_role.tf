# IAM Role for EMR Notebook with required permissions
resource "aws_iam_role" "shc_emr_notebook_role" {
  name = var.role_name

  # Trust relationship policy
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          Service = "elasticmapreduce.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = var.tags
}

# Attach AmazonElasticMapReduceRole policy
resource "aws_iam_role_policy_attachment" "emr_role_policy" {
  role       = aws_iam_role.shc_emr_notebook_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonElasticMapReduceRole"
}

# Attach AmazonS3FullAccess policy
resource "aws_iam_role_policy_attachment" "s3_full_access_policy" {
  role       = aws_iam_role.shc_emr_notebook_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonS3FullAccess"
}

# Output the role ARN for reference
output "emr_notebook_role_arn" {
  description = "ARN of the EMR Notebook IAM role"
  value       = aws_iam_role.shc_emr_notebook_role.arn
}

output "emr_notebook_role_name" {
  description = "Name of the EMR Notebook IAM role"
  value       = aws_iam_role.shc_emr_notebook_role.name
}