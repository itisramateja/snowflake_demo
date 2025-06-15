#!/usr/bin/env python3
"""
EventCombo ETL Job - Improved Version

This script extracts event data from EventCombo API and uploads it to S3.
Improvements include:
- Proper secrets management
- Better error handling and logging
- Security enhancements
- Code quality improvements
- Configuration management
"""

import os
import sys
import json
import time
import random
import logging
import tempfile
from datetime import datetime, timedelta, timezone
from typing import Optional, Dict, Any
from pathlib import Path

import requests
import boto3
from botocore.exceptions import ClientError, BotoCoreError


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('eventcombo_etl.log')
    ]
)
logger = logging.getLogger(__name__)


class EventComboETLError(Exception):
    """Custom exception for EventCombo ETL operations"""
    pass


class SecretsManager:
    """Handles AWS Secrets Manager operations"""
    
    def __init__(self, region_name: str = "us-west-2"):
        self.region_name = region_name
        self.session = boto3.session.Session()
        self.client = self.session.client(
            service_name='secretsmanager', 
            region_name=region_name
        )
    
    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        """Retrieve secret from AWS Secrets Manager"""
        try:
            logger.info(f"Retrieving secret: {secret_name}")
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            error_code = e.response['Error']['Code']
            logger.error(f"Failed to retrieve secret {secret_name}: {error_code}")
            raise EventComboETLError(f"Secret retrieval failed: {error_code}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse secret JSON for {secret_name}")
            raise EventComboETLError("Invalid secret format") from e


class EventComboAPI:
    """Handles EventCombo API operations"""
    
    def __init__(self, base_url: str = "https://www.eventcombo.com"):
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.access_token: Optional[str] = None
        
        # Set default headers
        self.session.headers.update({
            'User-Agent': 'EventCombo-ETL/1.0',
            'Accept': 'application/json'
        })
    
    def authenticate(self, username: str, password: str) -> bool:
        """Authenticate with EventCombo API and store access token"""
        url = f"{self.base_url}/API/Token"
        
        payload = {
            "grant_type": "password",
            "username": username,
            "password": password
        }
        
        headers = {
            "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
        }
        
        try:
            logger.info("Attempting authentication with EventCombo API")
            response = self.session.post(url, data=payload, headers=headers, timeout=30)
            response.raise_for_status()
            
            token_data = response.json()
            self.access_token = token_data.get("access_token")
            
            if not self.access_token:
                raise EventComboETLError("No access token in response")
            
            # Update session headers with auth token
            self.session.headers.update({
                "Authorization": f"Bearer {self.access_token}"
            })
            
            logger.info("Authentication successful")
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Authentication request failed: {e}")
            raise EventComboETLError(f"Authentication failed: {e}") from e
        except (KeyError, json.JSONDecodeError) as e:
            logger.error(f"Invalid authentication response: {e}")
            raise EventComboETLError("Invalid authentication response") from e
    
    def get_event_list(self) -> Dict[str, Any]:
        """Retrieve event list from EventCombo API"""
        if not self.access_token:
            raise EventComboETLError("Not authenticated. Call authenticate() first.")
        
        url = f"{self.base_url}/api/v2/Public/Event/List"
        
        try:
            logger.info("Fetching event list from EventCombo API")
            response = self.session.get(url, timeout=60)
            response.raise_for_status()
            
            data = response.json()
            logger.info(f"Successfully retrieved event list with {len(data.get('events', []))} events")
            return data
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch event list: {e}")
            raise EventComboETLError(f"API request failed: {e}") from e
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON response: {e}")
            raise EventComboETLError("Invalid API response format") from e


class S3Uploader:
    """Handles S3 upload operations"""
    
    def __init__(self, bucket_name: str, region_name: str = "us-west-2"):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client('s3', region_name=region_name)
    
    def upload_json_data(self, data: Dict[str, Any], s3_key: str) -> bool:
        """Upload JSON data to S3"""
        try:
            # Use temporary file for better memory management
            with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as temp_file:
                json.dump(data, temp_file, indent=2, default=str)
                temp_file_path = temp_file.name
            
            try:
                # Upload to S3
                logger.info(f"Uploading data to S3: s3://{self.bucket_name}/{s3_key}")
                with open(temp_file_path, 'rb') as file:
                    self.s3_client.put_object(
                        Body=file,
                        Bucket=self.bucket_name,
                        Key=s3_key,
                        ContentType='application/json'
                    )
                
                logger.info(f"Successfully uploaded to S3: {s3_key}")
                return True
                
            finally:
                # Clean up temporary file
                Path(temp_file_path).unlink(missing_ok=True)
                
        except (BotoCoreError, ClientError) as e:
            logger.error(f"S3 upload failed: {e}")
            raise EventComboETLError(f"S3 upload failed: {e}") from e
        except Exception as e:
            logger.error(f"Unexpected error during S3 upload: {e}")
            raise EventComboETLError(f"Upload failed: {e}") from e


class RetryHandler:
    """Handles retry logic with exponential backoff"""
    
    @staticmethod
    def retry_with_backoff(
        func, 
        *args, 
        max_retries: int = 3, 
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        **kwargs
    ):
        """Execute function with exponential backoff retry logic"""
        last_exception = None
        
        for attempt in range(max_retries + 1):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                last_exception = e
                
                if attempt == max_retries:
                    func_name = getattr(func, '__name__', str(func))
                    logger.error(f"Max retries ({max_retries}) exceeded for {func_name}")
                    break
                
                delay = min(base_delay * (2 ** attempt) + random.uniform(0, 1), max_delay)
                func_name = getattr(func, '__name__', str(func))
                logger.warning(f"Attempt {attempt + 1} failed for {func_name}: {e}. Retrying in {delay:.2f}s")
                time.sleep(delay)
        
        func_name = getattr(func, '__name__', str(func))
        raise EventComboETLError(f"Function {func_name} failed after {max_retries} retries") from last_exception


class EventComboETL:
    """Main ETL orchestrator"""
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        self.config = config or self._load_config()
        self.secrets_manager = SecretsManager(self.config.get('aws_region', 'us-west-2'))
        self.api = EventComboAPI(self.config.get('eventcombo_base_url', 'https://www.eventcombo.com'))
        self.s3_uploader = S3Uploader(
            self.config['s3_bucket'],
            self.config.get('aws_region', 'us-west-2')
        )
    
    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from environment variables"""
        return {
            'secret_name': os.getenv('EVENTCOMBO_SECRET_NAME', 'eventcombo'),
            's3_bucket': os.getenv('S3_BUCKET', 'shc-ea-fivetran'),
            's3_key_prefix': os.getenv('S3_KEY_PREFIX', 'fivetran/eventcombo'),
            'aws_region': os.getenv('AWS_REGION', 'us-west-2'),
            'eventcombo_base_url': os.getenv('EVENTCOMBO_BASE_URL', 'https://www.eventcombo.com'),
            'max_retries': int(os.getenv('MAX_RETRIES', '3')),
        }
    
    def _get_credentials(self) -> Dict[str, str]:
        """Get credentials from AWS Secrets Manager"""
        try:
            secret_data = self.secrets_manager.get_secret(self.config['secret_name'])
            
            required_keys = ['username', 'password']
            missing_keys = [key for key in required_keys if key not in secret_data]
            
            if missing_keys:
                raise EventComboETLError(f"Missing required keys in secret: {missing_keys}")
            
            return {
                'username': secret_data['username'],
                'password': secret_data['password']
            }
            
        except Exception as e:
            logger.error(f"Failed to retrieve credentials: {e}")
            raise
    
    def run(self) -> bool:
        """Execute the complete ETL process"""
        try:
            logger.info("Starting EventCombo ETL job")
            
            # Get credentials
            credentials = self._get_credentials()
            
            # Authenticate with API
            RetryHandler.retry_with_backoff(
                self.api.authenticate,
                credentials['username'],
                credentials['password'],
                max_retries=self.config['max_retries']
            )
            
            # Fetch event data
            event_data = RetryHandler.retry_with_backoff(
                self.api.get_event_list,
                max_retries=self.config['max_retries']
            )
            
            # Generate S3 key with timestamp
            timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
            s3_key = f"{self.config['s3_key_prefix']}/eventlist_{timestamp}.json"
            
            # Upload to S3
            RetryHandler.retry_with_backoff(
                self.s3_uploader.upload_json_data,
                event_data,
                s3_key,
                max_retries=self.config['max_retries']
            )
            
            logger.info("EventCombo ETL job completed successfully")
            return True
            
        except Exception as e:
            logger.error(f"ETL job failed: {e}")
            raise


def main():
    """Main entry point"""
    try:
        etl = EventComboETL()
        success = etl.run()
        sys.exit(0 if success else 1)
        
    except KeyboardInterrupt:
        logger.info("ETL job interrupted by user")
        sys.exit(130)
    except Exception as e:
        logger.error(f"ETL job failed with unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()