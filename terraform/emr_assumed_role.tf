# Custom IAM policy for Amazon MWAA Full Console Access
resource "aws_iam_policy" "amazon_mwaa_full_console_access" {
  name        = "AmazonMWAAFullConsoleAccess"
  description = "Custom policy providing full console access to Amazon MWAA"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = "airflow:*"
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:ListRoles"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:CreatePolicy"
        ]
        Resource = "arn:aws:iam::533527793305:policy/service-role/MWAA-Execution-Policy*"
      },
      {
        Effect = "Allow"
        Action = [
          "iam:CreateServiceLinkedRole"
        ]
        Resource = "arn:aws:iam::*:role/aws-service-role/airflow.amazonaws.com/AWSServiceRoleForAmazonMWAA"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetBucketLocation",
          "s3:ListAllMyBuckets",
          "s3:ListBucket",
          "s3:ListBucketVersions"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:CreateBucket",
          "s3:PutObject",
          "s3:GetEncryptionConfiguration"
        ]
        Resource = "arn:aws:s3:::*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:DescribeSecurityGroups",
          "ec2:DescribeSubnets",
          "ec2:DescribeVpcs",
          "ec2:DescribeRouteTables"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:AuthorizeSecurityGroupIngress",
          "ec2:CreateSecurityGroup"
        ]
        Resource = "arn:aws:ec2:*:*:security-group/airflow-security-group-*"
      },
      {
        Effect = "Allow"
        Action = [
          "kms:ListAliases"
        ]
        Resource = "*"
      },
      {
        Effect = "Allow"
        Action = [
          "kms:DescribeKey",
          "kms:ListGrants",
          "kms:CreateGrant",
          "kms:RevokeGrant",
          "kms:Decrypt",
          "kms:Encrypt",
          "kms:GenerateDataKey*",
          "kms:ReEncrypt*"
        ]
        Resource = [
          "arn:aws:kms:*:533527793305:key/15ac4a18-4f7b-4ebd-9e07-f873ea63408f",
          "arn:aws:kms:*:533527793305:key/5da753c3-3eeb-4b94-a67d-307616adea3e",
          "arn:aws:kms:us-west-2:533527793305:key/27a60ff2-e6e3-40c3-a01f-c5c4705ccc70"
        ]
      },
      {
        Effect   = "Allow"
        Action   = ["iam:PassRole"]
        Resource = "*"
        Condition = {
          StringLike = {
            "iam:PassedToService" = "airflow.amazonaws.com"
          }
        }
      },
      {
        Effect = "Allow"
        Action = [
          "iam:AttachRolePolicy",
          "iam:CreateRole"
        ]
        Resource = "arn:aws:iam::533527793305:role/service-role/AmazonMWAA*"
      },
      {
        Effect = "Allow"
        Action = [
          "s3:GetEncryptionConfiguration"
        ]
        Resource = "arn:aws:s3:::*"
      },
      {
        Effect = "Allow"
        Action = "ec2:CreateVpcEndpoint"
        Resource = [
          "arn:aws:ec2:*:*:vpc-endpoint/*",
          "arn:aws:ec2:*:*:vpc/*",
          "arn:aws:ec2:*:*:subnet/*",
          "arn:aws:ec2:*:*:security-group/*"
        ]
      },
      {
        Effect = "Allow"
        Action = [
          "ec2:CreateNetworkInterface"
        ]
        Resource = [
          "arn:aws:ec2:*:*:subnet/*",
          "arn:aws:ec2:*:*:network-interface/*"
        ]
      }
    ]
  })

  tags = {
    Name        = "AmazonMWAAFullConsoleAccess"
    Description = "Custom policy for Amazon MWAA full console access"
    Purpose     = "EMR-AssumedRole"
  }
}

# Custom IAM policy for Amazon MWAA Web Server Access
resource "aws_iam_policy" "amazon_mwaa_web_server_access" {
  name        = "AmazonMWAAWebServerAccess"
  description = "Custom policy providing web server access to Amazon MWAA environments"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "airflow:CreateWebLoginToken"
        Resource = [
          "arn:aws:airflow:us-west-2:533527793305:role/shc-nonprod-mwaa/Admin",
          "arn:aws:airflow:us-west-2:533527793305:role/shc-prod-mwaa/Admin",
          "arn:aws:airflow:us-west-2:533527793305:role/shc-test-mwaa/Admin"
        ]
      }
    ]
  })

  tags = {
    Name        = "AmazonMWAAWebServerAccess"
    Description = "Custom policy for Amazon MWAA web server access"
    Purpose     = "EMR-AssumedRole"
  }
}

# Custom IAM policy for EC2 operations
resource "aws_iam_policy" "customer_inline_ec2" {
  name        = "Customerinlineec2"
  description = "Custom policy providing comprehensive EC2 management permissions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = [
          "ec2:StopInstances",
          "ec2:StartInstances",
          "ec2:RebootInstances",
          "ec2:GetConsoleScreenshot"
        ]
        Resource = [
          "arn:aws:ec2:*:*:instance/*"
        ]
      },
      {
        Sid    = "AllowDescribe"
        Effect = "Allow"
        Action = [
          "ec2:Describe*"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Sid    = "RunInstances"
        Effect = "Allow"
        Action = "ec2:RunInstances"
        Resource = [
          "arn:aws:ec2:*:*:instance/*",
          "arn:aws:ec2:*:*:volume/*",
          "arn:aws:ec2:*:*:subnet/*",
          "arn:aws:ec2:*:*:network-interface/*",
          "arn:aws:ec2:*:*:key-pair/*",
          "arn:aws:ec2:*:*:security-group/*",
          "arn:aws:ec2:*:*:launch-template/*"
        ]
      },
      {
        Sid    = "ModifyInstanceAttribute"
        Effect = "Allow"
        Action = [
          "ec2:ModifyInstanceAttribute",
          "ec2:UnmonitorInstances",
          "ec2:MonitorInstances"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Sid    = "GetWindowsPassword"
        Effect = "Allow"
        Action = "ec2:GetPasswordData"
        Resource = [
          "*"
        ]
      },
      {
        Sid    = "AllowSpinupOfTaggedCleardataAMIs"
        Effect = "Allow"
        Action = [
          "ec2:RunInstances"
        ]
        Resource = [
          "arn:aws:ec2:*::image/ami-*"
        ]
        Condition = {
          StringEquals = {
            "ec2:ResourceTag/cleardata:hardened" = "1"
          }
        }
      },
      {
        Sid    = "AllowSpinupOfSharedCleardataAMIs"
        Effect = "Allow"
        Action = [
          "ec2:RunInstances"
        ]
        Resource = [
          "arn:aws:ec2:*::image/ami-*"
        ]
        Condition = {
          StringEquals = {
            "ec2:Owner" = "298058684257"
          }
        }
      },
      {
        Sid    = "AllowTagChanges"
        Effect = "Allow"
        Action = [
          "ec2:DeleteTags",
          "ec2:CreateTags"
        ]
        Resource = "*"
      },
      {
        Sid    = "DontTouchVPCTags"
        Effect = "Deny"
        Action = [
          "ec2:CreateTags",
          "ec2:DeleteTags"
        ]
        Resource = "arn:aws:ec2:*:*:vpc/*"
      },
      {
        Sid    = "AllowEbsModification"
        Effect = "Allow"
        Action = [
          "ec2:AttachVolume",
          "ec2:CreateVolume",
          "ec2:DeleteVolume",
          "ec2:ModifyVolume",
          "ec2:ModifyVolumeAttribute",
          "ec2:DescribeVolumes",
          "ec2:DescribeVolumeAttribute",
          "ec2:EnableVolumeIO",
          "ec2:DetachVolume"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Sid    = "AllowKill"
        Effect = "Allow"
        Action = [
          "ec2:StopInstances",
          "ec2:TerminateInstances",
          "ec2:DeleteVolume",
          "ec2:DetachVolume",
          "ec2:DescribeVolumes",
          "ec2:DescribeVolumeStatus",
          "ec2:DescribeVolumeAttribute"
        ]
        Resource = [
          "arn:aws:ec2:*:*:instance/*",
          "arn:aws:ec2:*:*:volume/*"
        ]
      },
      {
        Sid    = "AllowDecodingErrors"
        Effect = "Allow"
        Action = [
          "sts:DecodeAuthorizationMessage"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Sid = "CreateAMIs"
        Action = [
          "ec2:CreateImage",
          "ec2:CopyImage",
          "ec2:DescribeImageAttribute",
          "ec2:DescribeImages",
          "ec2:ModifyImageAttribute",
          "ec2:RegisterImage",
          "ec2:ResetImageAttribute"
        ]
        Effect   = "Allow"
        Resource = "*"
      },
      {
        Effect   = "Allow"
        Action   = "autoscaling:*"
        Resource = "*"
      },
      {
        Sid    = "AllowListInstanceProfile"
        Effect = "Allow"
        Action = [
          "iam:ListInstanceProfiles"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Sid    = "AllowHealth"
        Effect = "Allow"
        Action = [
          "health:*"
        ]
        Resource = [
          "*"
        ]
      },
      {
        Sid    = "AllowKeyPair"
        Effect = "Allow"
        Action = [
          "ec2:DescribeKeyPairs",
          "ec2:CreateKeyPair"
        ]
        Resource = [
          "*"
        ]
      }
    ]
  })

  tags = {
    Name        = "Customerinlineec2"
    Description = "Custom policy for comprehensive EC2 management"
    Purpose     = "EMR-AssumedRole"
  }
}

# Custom IAM policy for DataRobot S3 access
resource "aws_iam_policy" "shc_datarobot_s3" {
  name        = "SHC-Datarobot-S3"
  description = "Custom policy providing S3 access for DataRobot operations"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "AllowAccessToProduction"
        Effect = "Allow"
        Action = [
          "s3:DeleteObject",
          "s3:Get*",
          "s3:PutObject",
          "s3:ReplicateDelete",
          "s3:ListMultipartUploadParts"
        ]
        Resource = [
          "arn:aws:s3:::vertex-storage-cts/*",
          "arn:aws:s3:::shc-dts-projects/*",
          "arn:aws:s3:::shc-ds-datarobot/*",
          "arn:aws:s3:::shc-ea-snowflake/*"
        ]
      },
      {
        Sid    = "AllowListBucketsProduction"
        Effect = "Allow"
        Action = [
          "s3:ListBucket",
          "s3:ListBucketVersions",
          "s3:ListAllMyBuckets"
        ]
        Resource = [
          "arn:aws:s3:::*"
        ]
      }
    ]
  })

  tags = {
    Name        = "SHC-Datarobot-S3"
    Description = "Custom policy for DataRobot S3 access"
    Purpose     = "EMR-AssumedRole"
  }
}

# Custom IAM policy for Data Science operations
resource "aws_iam_policy" "shc_ds_policies" {
  name        = "SHC-DS-Policies"
  description = "Custom policy providing comprehensive data science and ML operations permissions"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "VisualEditor0"
        Effect = "Allow"
        Action = "iam:PassRole"
        Resource = [
          "arn:aws:iam::533527793305:instance-profile/datarobot-prod-stack-IAMStack-36EC7JB6J72X-InstanceProfile-1HYEM76JQ6LZV",
          "arn:aws:iam::533527793305:role/datarobot-prod-stack-IAMStack-36E-DataRobotIAMRole-1XD5JJ0S70W9H"
        ]
      },
      {
        Sid    = "VisualEditor1"
        Effect = "Allow"
        Action = [
          "iam:ListRole*",
          "iam:CreateRole",
          "codeartifact:*",
          "secretsmanager:UpdateSecret*",
          "cloudwatch:GetMetricData",
          "logs:*",
          "autoscaling:*",
          "comprehend:*",
          "lambda:*",
          "sagemaker:*",
          "ec2:*",
          "geo:*",
          "secretsmanager:Create*",
          "iam:GetRole*",
          "secretsmanager:ListSecrets",
          "bedrock:*"
        ]
        Resource = "*"
      },
      {
        Sid      = "VisualEditor2"
        Effect   = "Allow"
        Action   = "sts:GetServiceBearerToken"
        Resource = "*"
        Condition = {
          StringEquals = {
            "sts:AWSServiceName" = "codeartifact.amazonaws.com"
          }
        }
      },
      {
        Sid    = "VisualEditor3"
        Effect = "Allow"
        Action = "secretsmanager:*"
        Resource = [
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:ecs-task-dev-dbtoncloud/dev/SFLKConn/dbtoncloud-quZfDP",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:GITTOKEN_DS-ZIN8K3",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:shc-snowflake-Heb6kD",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:datarobot-chirm-6BkUos",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:imo-client-D9y2eG",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:contentful-sSEdFc",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:windowsdefender-DoA7NI",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:mdstaff-vjClHU",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:vizient_risk_api-f3HUFw",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:providers_api-9N2KfO",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:talkdesk-0jhEfb",
          "arn:aws:secretsmanager:us-west-2:533527793305:secret:eventcombo-mVK3sQ"
        ]
      },
      {
        Sid    = "VisualEditor4"
        Effect = "Allow"
        Action = "s3:*"
        Resource = [
          "arn:aws:s3:::shc-ea-fivetran/*",
          "arn:aws:s3:::shc-ea-fivetran"
        ]
      }
    ]
  })

  tags = {
    Name        = "SHC-DS-Policies"
    Description = "Custom policy for data science and ML operations"
    Purpose     = "EMR-AssumedRole"
  }
}

# Custom IAM policy for Data Science SSM operations
resource "aws_iam_policy" "shc_ds_ssm_policy" {
  name        = "SHC-DS-SSM-Policy"
  description = "Custom policy providing SSM and EC2 access for data science operations"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "VisualEditor0"
        Effect = "Allow"
        Action = [
          "ec2:RebootInstances",
          "ec2:StartInstances",
          "ec2:StopInstances"
        ]
        Resource = "arn:aws:ec2:us-west-2:533527793305:instance/*"
        Condition = {
          StringEquals = {
            "aws:ResourceTag/environment" = "non-prod"
          }
        }
      },
      {
        Sid    = "VisualEditor1"
        Effect = "Allow"
        Action = [
          "s3:GetAccessPoint",
          "ec2:DescribeInstances",
          "ssm:GetConnectionStatus",
          "s3:ListAccessPoints",
          "ec2:DescribeTags",
          "ssm:DescribeSessions",
          "s3:ListJobs",
          "elasticmapreduce:RunJobFlow",
          "ec2:DescribeInstanceStatus",
          "ssm:DescribeInstanceProperties"
        ]
        Resource = "*"
      },
      {
        Sid    = "VisualEditor2"
        Effect = "Allow"
        Action = [
          "s3:PutAnalyticsConfiguration",
          "s3:PutAccessPointConfigurationForObjectLambda",
          "s3:GetObjectVersionTagging",
          "s3:CreateBucket",
          "elasticmapreduce:CreateEditor",
          "s3:GetStorageLensConfigurationTagging",
          "s3:ReplicateObject",
          "s3:GetObjectAcl",
          "s3:GetBucketObjectLockConfiguration",
          "s3:GetIntelligentTieringConfiguration",
          "s3:PutLifecycleConfiguration",
          "s3:GetObjectVersionAcl",
          "s3:DeleteObject",
          "s3:GetBucketPolicyStatus",
          "s3:GetObjectRetention",
          "s3:GetBucketWebsite",
          "s3:GetJobTagging",
          "s3:PutReplicationConfiguration",
          "s3:PutObjectLegalHold",
          "s3:GetObjectLegalHold",
          "s3:GetBucketNotification",
          "s3:PutBucketCORS",
          "s3:GetReplicationConfiguration",
          "s3:ListMultipartUploadParts",
          "s3:PutObject",
          "s3:GetObject",
          "s3:PutBucketNotification",
          "elasticmapreduce:StartEditor",
          "s3:DescribeJob",
          "s3:PutBucketLogging",
          "s3:GetAnalyticsConfiguration",
          "s3:PutBucketObjectLockConfiguration",
          "s3:GetObjectVersionForReplication",
          "s3:GetAccessPointForObjectLambda",
          "s3:GetStorageLensDashboard",
          "s3:CreateAccessPoint",
          "s3:GetLifecycleConfiguration",
          "s3:GetInventoryConfiguration",
          "s3:GetBucketTagging",
          "s3:PutAccelerateConfiguration",
          "s3:GetAccessPointPolicyForObjectLambda",
          "s3:GetBucketLogging",
          "s3:ListBucketVersions",
          "s3:RestoreObject",
          "s3:ListBucket",
          "s3:GetAccelerateConfiguration",
          "s3:GetBucketPolicy",
          "s3:PutEncryptionConfiguration",
          "s3:GetEncryptionConfiguration",
          "s3:GetObjectVersionTorrent",
          "s3:AbortMultipartUpload",
          "s3:GetBucketRequestPayment",
          "s3:GetAccessPointPolicyStatus",
          "elasticmapreduce:StopEditor",
          "s3:UpdateJobPriority",
          "s3:GetObjectTagging",
          "s3:GetMetricsConfiguration",
          "s3:GetBucketOwnershipControls",
          "s3:PutBucketVersioning",
          "s3:GetBucketPublicAccessBlock",
          "s3:ListBucketMultipartUploads",
          "s3:PutIntelligentTieringConfiguration",
          "s3:GetAccessPointPolicyStatusForObjectLambda",
          "s3:PutMetricsConfiguration",
          "elasticmapreduce:OpenEditorInConsole",
          "s3:PutBucketOwnershipControls",
          "s3:UpdateJobStatus",
          "s3:GetBucketVersioning",
          "s3:GetBucketAcl",
          "s3:GetAccessPointConfigurationForObjectLambda",
          "s3:PutInventoryConfiguration",
          "s3:GetObjectTorrent",
          "s3:GetStorageLensConfiguration",
          "s3:PutBucketWebsite",
          "s3:PutBucketRequestPayment",
          "s3:PutObjectRetention",
          "s3:CreateAccessPointForObjectLambda",
          "s3:GetBucketCORS",
          "elasticmapreduce:AddJobFlowSteps",
          "s3:GetBucketLocation",
          "s3:GetAccessPointPolicy",
          "s3:ReplicateDelete",
          "s3:GetObjectVersion"
        ]
        Resource = [
          "arn:aws:elasticmapreduce:*:533527793305:cluster/*",
          "arn:aws:elasticmapreduce:*:533527793305:editor/*",
          "arn:aws:s3:::shc-ds-*",
          "arn:aws:s3:::shc-ds*/*"
        ]
      },
      {
        Sid    = "AllowDatarobotConsoleSessions"
        Effect = "Allow"
        Action = "ssm:StartSession"
        Resource = [
          "arn:aws:ec2:us-west-2:533527793305:instance/*"
        ]
        Condition = {
          StringEquals = {
            "aws:ResourceTag/Project" = "datarobot"
          }
        }
      },
      {
        Sid    = "AllowConsoleSessionsSSMDocuments"
        Effect = "Allow"
        Action = "ssm:StartSession"
        Resource = [
          "arn:aws:ssm:us-west-2::document/AWS-StartSSHSession",
          "arn:aws:ssm:us-west-2:533527793305:document/SSM-SessionManagerRunShell"
        ]
      },
      {
        Sid    = "VisualEditor5"
        Effect = "Allow"
        Action = [
          "ssm:GetDocument",
          "ssm:UpdateDocument",
          "ssm:CreateDocument"
        ]
        Resource = "arn:aws:ssm:us-west-2:533527793305:document/SSM-SessionManagerRunShell"
      },
      {
        Sid      = "VisualEditor6"
        Effect   = "Allow"
        Action   = "ssm:TerminateSession"
        Resource = "arn:aws:ssm:*:*:session/$${aws:username}-*"
      }
    ]
  })

  tags = {
    Name        = "SHC-DS-SSM-Policy"
    Description = "Custom policy for data science SSM and EC2 operations"
    Purpose     = "EMR-AssumedRole"
  }
}

# Custom IAM policy for MWAA CloudWatch Logs access
resource "aws_iam_policy" "shc_mwaa_cloudwatch_logs" {
  name        = "SHC-MWAA-Cloudwatch-Logs"
  description = "Custom policy providing CloudWatch Logs access for MWAA operations"

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "VisualEditor0"
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents",
          "logs:PutLogEvents"
        ]
        Resource = [
          "arn:aws:logs:us-west-2:533527793305:log-group:airflow-shc-nonprod-mwaa-*",
          "arn:aws:logs:*:533527793305:log-group:*:log-stream:*"
        ]
      },
      {
        Sid    = "VisualEditor1"
        Effect = "Allow"
        Action = [
          "logs:CreateLogStream",
          "logs:DescribeLogGroups",
          "logs:DescribeLogStreams",
          "logs:GetLogEvents",
          "logs:PutLogEvents"
        ]
        Resource = "arn:aws:logs:us-west-2:533527793305:log-group:airflow-shc-nonprod-mwaa-*"
      }
    ]
  })

  tags = {
    Name        = "SHC-MWAA-Cloudwatch-Logs"
    Description = "Custom policy for MWAA CloudWatch Logs access"
    Purpose     = "EMR-AssumedRole"
  }
}

# IAM Role for EMR Assumed Role with MWAA permissions
resource "aws_iam_role" "shc_emr_assumed_role" {
  name = var.emr_assumed_role_name

  # Trust relationship policy - allowing specific roles and EMR service to assume the role
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Principal = {
          AWS = [
            "arn:aws:iam::533527793305:role/SSO-SHC-READONLY",
            "arn:aws:iam::533527793305:role/SHC-DTS-Admins"
          ]
          Service = "elasticmapreduce.amazonaws.com"
        }
        Action = "sts:AssumeRole"
      }
    ]
  })

  tags = merge(var.tags, {
    Name = var.emr_assumed_role_name
    Type = "AssumedRole"
  })
}

# Attach AmazonElasticMapReduceEditorsRole policy
resource "aws_iam_role_policy_attachment" "emr_editors_role_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonElasticMapReduceEditorsRole"
}

# Attach AmazonElasticMapReduceReadOnlyAccess policy
resource "aws_iam_role_policy_attachment" "emr_readonly_access_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = "arn:aws:iam::aws:policy/AmazonElasticMapReduceReadOnlyAccess"
}

# Attach custom AmazonMWAAFullConsoleAccess policy
resource "aws_iam_role_policy_attachment" "mwaa_full_console_access_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.amazon_mwaa_full_console_access.arn
}

# Attach custom AmazonMWAAWebServerAccess policy
resource "aws_iam_role_policy_attachment" "mwaa_web_server_access_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.amazon_mwaa_web_server_access.arn
}

# Attach custom Customerinlineec2 policy
resource "aws_iam_role_policy_attachment" "customer_inline_ec2_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.customer_inline_ec2.arn
}

# Attach custom SHC-Datarobot-S3 policy
resource "aws_iam_role_policy_attachment" "shc_datarobot_s3_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.shc_datarobot_s3.arn
}

# Attach custom SHC-DS-Policies policy
resource "aws_iam_role_policy_attachment" "shc_ds_policies_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.shc_ds_policies.arn
}

# Attach custom SHC-DS-SSM-Policy policy
resource "aws_iam_role_policy_attachment" "shc_ds_ssm_policy_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.shc_ds_ssm_policy.arn
}

# Attach custom SHC-MWAA-Cloudwatch-Logs policy
resource "aws_iam_role_policy_attachment" "shc_mwaa_cloudwatch_logs_policy" {
  role       = aws_iam_role.shc_emr_assumed_role.name
  policy_arn = aws_iam_policy.shc_mwaa_cloudwatch_logs.arn
}

# Output the assumed role ARN for reference
output "emr_assumed_role_arn" {
  description = "ARN of the EMR Assumed Role"
  value       = aws_iam_role.shc_emr_assumed_role.arn
}

output "emr_assumed_role_name" {
  description = "Name of the EMR Assumed Role"
  value       = aws_iam_role.shc_emr_assumed_role.name
}

output "mwaa_policy_arn" {
  description = "ARN of the custom MWAA Full Console Access policy"
  value       = aws_iam_policy.amazon_mwaa_full_console_access.arn
}

output "mwaa_web_server_policy_arn" {
  description = "ARN of the custom MWAA Web Server Access policy"
  value       = aws_iam_policy.amazon_mwaa_web_server_access.arn
}

output "customer_inline_ec2_policy_arn" {
  description = "ARN of the custom EC2 inline policy"
  value       = aws_iam_policy.customer_inline_ec2.arn
}

output "shc_datarobot_s3_policy_arn" {
  description = "ARN of the custom DataRobot S3 policy"
  value       = aws_iam_policy.shc_datarobot_s3.arn
}

output "shc_ds_policies_policy_arn" {
  description = "ARN of the custom Data Science policies"
  value       = aws_iam_policy.shc_ds_policies.arn
}

output "shc_ds_ssm_policy_arn" {
  description = "ARN of the custom Data Science SSM policy"
  value       = aws_iam_policy.shc_ds_ssm_policy.arn
}

output "shc_mwaa_cloudwatch_logs_policy_arn" {
  description = "ARN of the custom MWAA CloudWatch Logs policy"
  value       = aws_iam_policy.shc_mwaa_cloudwatch_logs.arn
}