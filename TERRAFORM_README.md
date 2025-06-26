# AWS Secrets Manager Terraform Configuration

This Terraform configuration manages AWS Secrets Manager secrets for the Snowflake Demo project. It creates and manages 25 different secrets used across various services and environments.

## 📁 File Structure

```
├── providers.tf          # Terraform and AWS provider configuration
├── variables.tf          # Variable definitions and defaults
├── secrets_manager.tf    # Main secrets configuration
└── TERRAFORM_README.md   # This documentation
```

## 🔐 Secrets Managed

### API and Service Secrets
- `eventcombo` - EventCombo service API credentials
- `providers_api` - External providers API credentials
- `talkdesk` - Talkdesk contact center platform credentials
- `xmatters/nonprod/api` - xMatters non-production API credentials
- `contentful` - Contentful CMS API credentials
- `windowsdefender` - Windows Defender ATP API credentials

### MDStaff Application Secrets
- `mdstaff` - Main application credentials
- `mdstaff-api` - API service credentials
- `mdstaff-client` - Client application credentials

### Vizient Integration Secrets
- `vizient_risk_api` - Vizient Risk API credentials
- `viz-api-cdb-credentials` - Vizient API CouchDB credentials
- `viz-api` - Vizient API service credentials

### Snowflake and Data Platform Secrets
- `sflk-svcdatahub` - Snowflake service account for DataHub
- `sflk-svc-user` - Snowflake service user
- `dbt_user` - DBT (Data Build Tool) user credentials
- `shc-snowflake` - SHC Snowflake connection credentials

### DataHub Secrets
- `prod/datahub_source_secrets` - DataHub data source connections
- `prod/datahub/secrets` - DataHub application secrets
- `shc-datahub-prod-opensearch` - DataHub OpenSearch cluster credentials

### Development and Deployment Secrets
- `prod/lookml-github-deploy-key` - LookML GitHub deployment key
- `ecs-task-dev-dbtoncloud/dev/SFLKConn/dbtoncloud` - ECS task DBT Cloud credentials

### AWS and Third-party Service Secrets
- `aws-s3-fivetran` - AWS S3 credentials for Fivetran
- `AmazonSageMaker-3f3c404d1fdf49d29b82332c9ea62032` - SageMaker credentials
- `imo-client` - IMO client credentials
- `healthy-places` - Healthy Places application credentials

## 🚀 Usage

### Prerequisites

1. **AWS CLI configured** with appropriate credentials
2. **Terraform installed** (version >= 1.0)
3. **Appropriate AWS permissions** for Secrets Manager operations

### Basic Deployment

1. **Initialize Terraform:**
   ```bash
   terraform init
   ```

2. **Review the plan:**
   ```bash
   terraform plan
   ```

3. **Apply the configuration:**
   ```bash
   terraform apply
   ```

### Customization

#### Environment Configuration
```hcl
# terraform.tfvars
environment = "production"
aws_region = "us-east-1"
recovery_window_in_days = 30

common_tags = {
  Project     = "snowflake_demo"
  ManagedBy   = "terraform"
  Owner       = "data-platform-team"
  Environment = "production"
}
```

#### Custom Secret Configuration
To add a new secret, update the `secrets_config` local in `secrets_manager.tf`:

```hcl
locals {
  secrets_config = {
    # ... existing secrets ...
    
    "new-secret-name" = {
      description = "Description of the new secret"
      tags = {
        Service = "service-name"
        Type    = "api-credentials"
      }
    }
  }
}
```

## 🏷️ Tagging Strategy

All secrets are tagged with:
- **Environment**: The deployment environment
- **Service**: The service that uses the secret
- **Type**: The type of credentials (api-credentials, service-account, etc.)
- **Component**: Specific component within a service (optional)
- **Organization**: Organization identifier (optional)

### Tag Types
- `api-credentials` - API keys and tokens
- `service-account` - Service account credentials
- `database-credentials` - Database connection credentials
- `client-credentials` - Client application credentials
- `deploy-key` - Deployment keys
- `task-credentials` - ECS task credentials
- `aws-credentials` - AWS service credentials
- `connection-credentials` - General connection credentials

## 📊 Outputs

The configuration provides several useful outputs:

- **`secret_arns`** - Map of secret names to ARNs
- **`secret_names`** - List of all secret names
- **`secrets_by_service`** - Secrets grouped by service
- **`secrets_by_type`** - Secrets grouped by credential type

### Example Output Usage
```bash
# Get all secret ARNs
terraform output secret_arns

# Get secrets for a specific service
terraform output secrets_by_service

# Get all API credential secrets
terraform output secrets_by_type
```

## 🔧 Configuration Options

### Variables

| Variable | Description | Default | Type |
|----------|-------------|---------|------|
| `environment` | Environment name | `"production"` | string |
| `aws_region` | AWS region | `"us-east-1"` | string |
| `recovery_window_in_days` | Secret recovery window | `30` | number |
| `common_tags` | Common tags for all resources | See variables.tf | map(string) |

### Recovery Window
- **0 days**: Immediate deletion (use with caution)
- **1-30 days**: Delayed deletion with recovery option
- **Default**: 30 days (recommended for production)

## 🔒 Security Best Practices

1. **Never commit actual secret values** to version control
2. **Use least privilege** IAM policies for Terraform execution
3. **Enable CloudTrail** for Secrets Manager API calls
4. **Rotate secrets regularly** using AWS Secrets Manager rotation
5. **Use separate environments** for dev/staging/production
6. **Monitor secret access** using CloudWatch logs

## 🔄 Secret Rotation

To enable automatic rotation for a secret:

```hcl
resource "aws_secretsmanager_secret_rotation" "example" {
  secret_id           = aws_secretsmanager_secret.secrets["secret-name"].id
  rotation_lambda_arn = aws_lambda_function.rotation_lambda.arn
  
  rotation_rules {
    automatically_after_days = 30
  }
}
```

## 🚨 Troubleshooting

### Common Issues

1. **Permission Denied**
   - Ensure AWS credentials have Secrets Manager permissions
   - Check IAM policies for `secretsmanager:*` actions

2. **Secret Already Exists**
   - Import existing secrets: `terraform import aws_secretsmanager_secret.secrets["name"] secret-arn`
   - Or use `terraform import` for existing resources

3. **Invalid Secret Name**
   - Secret names must be 1-512 characters
   - Can contain alphanumeric characters and `/_+=.@-`

### Useful Commands

```bash
# Check Terraform state
terraform state list

# Import existing secret
terraform import 'aws_secretsmanager_secret.secrets["secret-name"]' arn:aws:secretsmanager:region:account:secret:name

# Refresh state
terraform refresh

# Validate configuration
terraform validate
```

## 📝 Maintenance

### Adding New Secrets
1. Add to `secrets_config` in `secrets_manager.tf`
2. Run `terraform plan` to review changes
3. Apply with `terraform apply`

### Removing Secrets
1. Remove from `secrets_config`
2. Consider the recovery window before deletion
3. Ensure no applications depend on the secret

### Updating Descriptions or Tags
1. Modify the configuration in `secrets_config`
2. Apply changes with `terraform apply`

## 🤝 Contributing

When contributing to this configuration:

1. Follow the established naming conventions
2. Add appropriate tags for new secrets
3. Update this README for significant changes
4. Test changes in a non-production environment first

## 📞 Support

For issues or questions:
- Check the troubleshooting section above
- Review AWS Secrets Manager documentation
- Contact the data platform team

---

**Note**: This configuration manages secret metadata only. Actual secret values must be populated separately through the AWS Console, CLI, or application code.