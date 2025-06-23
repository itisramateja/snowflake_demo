# EMR IAM Roles Terraform Configuration

This Terraform configuration creates IAM roles for Amazon EMR operations with various permission levels and integrations.

## Resources Created

### 1. EMR Notebook Role: `SHC-EMR-NOTEBOOK-ROLE`
   - **Trust relationship**: Allows `elasticmapreduce.amazonaws.com` service to assume the role
   - **Policy Attachments**:
     - `AmazonElasticMapReduceRole` - Provides permissions for EMR operations
     - `AmazonS3FullAccess` - Provides full access to Amazon S3

### 2. EMR Assumed Role: `SHC-EMR-AssumedRole`
   - **Trust relationship**: Allows assumption by specific IAM roles (`SSO-SHC-READONLY`, `SHC-DTS-Admins`) and EMR service
   - **Policy Attachments**:
     - `AmazonElasticMapReduceEditorsRole` - Provides EMR editing permissions
     - `AmazonElasticMapReduceReadOnlyAccess` - Provides EMR read-only access
     - `AmazonMWAAFullConsoleAccess` (Custom) - Provides full Amazon MWAA console access
     - `AmazonMWAAWebServerAccess` (Custom) - Provides MWAA web login token creation
     - `Customerinlineec2` (Custom) - Provides comprehensive EC2 management permissions
     - `SHC-Datarobot-S3` (Custom) - Provides S3 access for DataRobot operations
     - `SHC-DS-Policies` (Custom) - Provides comprehensive data science and ML operations permissions
     - `SHC-DS-SSM-Policy` (Custom) - Provides SSM and EMR editor access for data science operations
     - `SHC-MWAA-Cloudwatch-Logs` (Custom) - Provides CloudWatch Logs access for MWAA operations

### 3. Custom IAM Policies

#### `AmazonMWAAFullConsoleAccess`
   - Comprehensive permissions for Amazon Managed Workflows for Apache Airflow (MWAA)
   - Includes S3, EC2, KMS, and IAM permissions required for MWAA operations

#### `AmazonMWAAWebServerAccess`
   - Allows creation of web login tokens for MWAA environments
   - Provides access to specific MWAA environments: shc-nonprod-mwaa, shc-prod-mwaa, shc-test-mwaa

#### `Customerinlineec2`
   - Comprehensive EC2 management permissions including instance lifecycle management
   - EBS volume operations, AMI creation, Auto Scaling, and key pair management
   - Includes specific conditions for hardened AMIs and shared AMI access
   - Contains security restrictions (e.g., VPC tag protection)

#### `SHC-Datarobot-S3`
   - S3 access permissions for DataRobot operations
   - Object-level permissions (Get, Put, Delete) for specific buckets: vertex-storage-cts, shc-dts-projects, shc-ds-datarobot, shc-ea-snowflake
   - Bucket listing permissions across all S3 buckets

#### `SHC-DS-Policies`
   - Comprehensive data science and machine learning operations permissions
   - IAM role passing for specific DataRobot roles and instance profiles
   - Full access to: SageMaker, Lambda, Comprehend, Bedrock, CodeArtifact, Auto Scaling
   - Secrets Manager access to specific application secrets
   - Full S3 access to shc-ea-fivetran bucket
   - CloudWatch metrics and logging permissions

#### `SHC-DS-SSM-Policy`
   - EC2 instance lifecycle management for non-prod environments (tagged with environment=non-prod)
   - SSM Session Manager access for DataRobot instances (tagged with Project=datarobot)
   - Comprehensive S3 permissions for shc-ds-* buckets
   - EMR editor and cluster management permissions
   - SSM document management for session management

#### `SHC-MWAA-Cloudwatch-Logs`
   - CloudWatch Logs access for MWAA operations
   - Log stream creation, reading, and writing permissions
   - Scoped to airflow-shc-nonprod-mwaa log groups
   - General log group and log stream describe permissions

## Files

- `main.tf` - Provider configuration
- `variables.tf` - Variable definitions
- `iam_role.tf` - EMR Notebook IAM role and policy attachments
- `emr_assumed_role.tf` - EMR Assumed Role and custom MWAA policy
- `README.md` - This documentation

## Usage

### Prerequisites

1. Install Terraform (>= 1.0)
2. Configure AWS credentials using one of these methods:
   - AWS CLI: `aws configure`
   - Environment variables: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_DEFAULT_REGION`
   - IAM roles (if running on EC2)

### Deployment Steps

1. Navigate to the terraform directory:
   ```bash
   cd terraform
   ```

2. Initialize Terraform:
   ```bash
   terraform init
   ```

3. Review the planned changes:
   ```bash
   terraform plan
   ```

4. Apply the configuration:
   ```bash
   terraform apply
   ```

5. Confirm the deployment by typing `yes` when prompted.

### Customization

You can customize the role names and tags by modifying the variables in `variables.tf` or by passing them during apply:

```bash
terraform apply -var="role_name=MY-CUSTOM-ROLE-NAME" -var="emr_assumed_role_name=MY-CUSTOM-ASSUMED-ROLE"
```

### Outputs

After successful deployment, the following outputs will be displayed:
- `emr_notebook_role_arn` - The ARN of the EMR Notebook IAM role
- `emr_notebook_role_name` - The name of the EMR Notebook IAM role
- `emr_assumed_role_arn` - The ARN of the EMR Assumed Role
- `emr_assumed_role_name` - The name of the EMR Assumed Role
- `mwaa_policy_arn` - The ARN of the custom MWAA Full Console Access policy
- `mwaa_web_server_policy_arn` - The ARN of the custom MWAA Web Server Access policy
- `customer_inline_ec2_policy_arn` - The ARN of the custom EC2 inline policy
- `shc_datarobot_s3_policy_arn` - The ARN of the custom DataRobot S3 policy
- `shc_ds_policies_policy_arn` - The ARN of the custom Data Science policies
- `shc_ds_ssm_policy_arn` - The ARN of the custom Data Science SSM policy
- `shc_mwaa_cloudwatch_logs_policy_arn` - The ARN of the custom MWAA CloudWatch Logs policy

### Cleanup

To destroy the created resources:
```bash
terraform destroy
```

## Security Considerations

### General Security
- **Principle of Least Privilege**: Review all permissions and remove any that are not strictly necessary for your use case.
- **Regular Auditing**: Regularly review and audit the permissions granted to these roles.
- **Controlled Access**: The assumed role can only be assumed by specific trusted roles, providing better security than account-wide access.

### Specific Policy Concerns
- **S3 Full Access**: The notebook role has `AmazonS3FullAccess` which provides broad S3 permissions. Consider using a more restrictive policy for production environments.
- **MWAA Custom Policies**: 
  - The MWAA Full Console Access policy includes broad permissions for KMS, S3, and EC2. Review the specific KMS key ARNs and ensure they match your environment.
  - The MWAA Web Server Access policy is scoped to specific environments but includes admin-level access.
- **EC2 Custom Policy**: The `Customerinlineec2` policy provides extensive EC2 permissions including:
  - Instance lifecycle management (start, stop, terminate, reboot)
  - EBS volume operations and AMI creation
  - Auto Scaling permissions
  - Broad EC2 describe permissions
- **DataRobot S3 Policy**: The `SHC-Datarobot-S3` policy provides:
  - Object-level access to specific production buckets
  - Broad bucket listing permissions across all S3 buckets
- **Data Science Policy**: The `SHC-DS-Policies` policy provides extensive permissions including:
  - Full access to multiple AWS ML/AI services (SageMaker, Bedrock, Comprehend)
  - Secrets Manager access to specific application secrets
  - IAM role passing capabilities for DataRobot operations
  - Full EC2 and Lambda permissions
- **SSM Policy**: The `SHC-DS-SSM-Policy` policy provides:
  - EC2 instance control limited to non-prod environments
  - SSM Session Manager access with resource-based conditions
  - Comprehensive S3 permissions for data science buckets
  - EMR editor and cluster management capabilities
- **CloudWatch Logs Policy**: The `SHC-MWAA-Cloudwatch-Logs` policy provides:
  - CloudWatch Logs access scoped to MWAA environments
  - Log stream creation and management permissions
- **Account-Specific Resources**: Policies contain hardcoded account IDs (533527793305) and specific resource ARNs. Update these for your environment.

### Trust Relationships
- **EMR Notebook Role**: Trusts the EMR service - appropriate for EMR operations.
- **EMR Assumed Role**: Trusts specific IAM roles (`SSO-SHC-READONLY`, `SHC-DTS-Admins`) and the EMR service. This provides controlled access to authorized roles only.

### Recommendations
1. **Update Environment-Specific Values**: Replace hardcoded account IDs, KMS key ARNs, and MWAA environment names to match your environment
2. **Review Trust Relationships**: Ensure the trusted roles (`SSO-SHC-READONLY`, `SHC-DTS-Admins`) exist in your AWS account before deployment
3. **Scope Down Permissions**: Consider implementing more restrictive policies based on actual usage patterns:
   - Replace S3 full access with bucket-specific permissions
   - Limit EC2 permissions to specific regions or resource tags
   - Restrict MWAA access to only required environments
   - Review DataRobot S3 bucket access and limit to necessary buckets only
   - Audit Secrets Manager access and remove unused secret ARNs
   - Consider restricting ML service permissions to specific resources where possible
   - Review SSM Session Manager access and ensure proper resource tagging
   - Limit CloudWatch Logs access to only required log groups
4. **Enable Monitoring**: 
   - Enable CloudTrail logging to monitor role usage
   - Set up CloudWatch alarms for unusual activity
5. **Regular Security Reviews**: 
   - Implement regular access reviews and permission audits
   - Monitor for unused permissions and remove them
6. **Resource Tagging**: Use consistent tagging strategies to enable better resource management and cost tracking