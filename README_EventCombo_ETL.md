# EventCombo ETL Job

This repository contains an improved version of the EventCombo ETL job that extracts event data from the EventCombo API and uploads it to AWS S3.

## Key Improvements

### Security Enhancements
- **Removed hardcoded credentials**: Uses AWS Secrets Manager for credential management
- **Proper error handling**: Sensitive information is not exposed in error messages
- **Secure session management**: Uses proper authentication tokens
- **Environment-based configuration**: Sensitive configuration moved to environment variables

### Code Quality Improvements
- **Proper logging**: Comprehensive logging with different levels
- **Error handling**: Custom exceptions and proper error propagation
- **Type hints**: Added type annotations for better code documentation
- **Class-based architecture**: Organized code into logical classes
- **Resource management**: Proper cleanup of temporary files
- **Retry mechanism**: Exponential backoff with configurable parameters

### Functional Improvements
- **Configuration management**: Environment-based configuration
- **Better S3 handling**: Uses temporary files and proper content types
- **Timestamped uploads**: Prevents file overwrites with timestamp-based naming
- **Memory efficiency**: Uses temporary files for large data processing

## Setup

### Prerequisites
- Python 3.7+
- AWS credentials configured (via AWS CLI, IAM role, or environment variables)
- Access to AWS Secrets Manager
- Access to target S3 bucket

### Installation
```bash
pip install -r requirements_eventcombo.txt
```

### Configuration

1. **AWS Secrets Manager Setup**:
   Create a secret in AWS Secrets Manager with the following structure:
   ```json
   {
     "username": "your-eventcombo-username",
     "password": "your-eventcombo-password"
   }
   ```

2. **Environment Variables**:
   Copy `.env.example` to `.env` and update with your values:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **AWS Permissions**:
   Ensure your AWS credentials have the following permissions:
   - `secretsmanager:GetSecretValue` for the EventCombo secret
   - `s3:PutObject` for the target S3 bucket

## Usage

### Basic Usage
```bash
python eventcombo_etl_improved.py
```

### With Custom Configuration
```bash
export EVENTCOMBO_SECRET_NAME=my-secret
export S3_BUCKET=my-bucket
python eventcombo_etl_improved.py
```

## Configuration Options

| Environment Variable | Default | Description |
|---------------------|---------|-------------|
| `EVENTCOMBO_SECRET_NAME` | `eventcombo` | Name of the AWS Secrets Manager secret |
| `S3_BUCKET` | `shc-ea-fivetran` | Target S3 bucket name |
| `S3_KEY_PREFIX` | `fivetran/eventcombo` | S3 key prefix for uploaded files |
| `AWS_REGION` | `us-west-2` | AWS region for services |
| `EVENTCOMBO_BASE_URL` | `https://www.eventcombo.com` | EventCombo API base URL |
| `MAX_RETRIES` | `3` | Maximum number of retry attempts |

## Logging

The application logs to both console and a file (`eventcombo_etl.log`). Log levels can be configured by modifying the logging configuration in the script.

## Error Handling

The improved version includes comprehensive error handling:
- **Authentication errors**: Proper handling of invalid credentials
- **API errors**: Retry logic with exponential backoff
- **S3 errors**: Detailed error messages for upload failures
- **Network errors**: Timeout and connection error handling

## Security Considerations

- Credentials are never stored in code or logs
- All API communications use HTTPS
- Temporary files are properly cleaned up
- Error messages don't expose sensitive information
- Uses AWS IAM for access control

## Monitoring and Alerting

Consider setting up:
- CloudWatch alarms for S3 upload failures
- Log monitoring for error patterns
- AWS Lambda for scheduled execution
- SNS notifications for job status

## Migration from Original Script

To migrate from the original script:

1. Set up AWS Secrets Manager with your credentials
2. Update environment variables as needed
3. Test the new script in a development environment
4. Replace the original script in your production environment

## Troubleshooting

### Common Issues

1. **Authentication Failed**:
   - Verify credentials in AWS Secrets Manager
   - Check secret name and region configuration

2. **S3 Upload Failed**:
   - Verify S3 bucket exists and is accessible
   - Check AWS credentials and permissions

3. **API Timeout**:
   - Check network connectivity
   - Verify EventCombo API status

### Debug Mode

Enable debug logging by modifying the logging level:
```python
logging.basicConfig(level=logging.DEBUG, ...)
```

## Contributing

When contributing to this project:
1. Follow the existing code style
2. Add appropriate error handling
3. Update documentation
4. Test security implications
5. Ensure no sensitive data is committed