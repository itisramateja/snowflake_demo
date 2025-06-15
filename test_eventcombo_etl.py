#!/usr/bin/env python3
"""
Test script for EventCombo ETL improvements
"""

import unittest
from unittest.mock import Mock, patch, MagicMock
import json
import tempfile
from pathlib import Path

# Import the classes from the improved ETL script
from eventcombo_etl_improved import (
    SecretsManager, 
    EventComboAPI, 
    S3Uploader, 
    RetryHandler,
    EventComboETL,
    EventComboETLError
)


class TestSecretsManager(unittest.TestCase):
    """Test SecretsManager functionality"""
    
    @patch('boto3.session.Session')
    def test_get_secret_success(self, mock_session):
        """Test successful secret retrieval"""
        # Mock the secrets manager client
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.return_value = {
            'SecretString': '{"username": "test", "password": "test123"}'
        }
        
        secrets_manager = SecretsManager()
        result = secrets_manager.get_secret("test-secret")
        
        self.assertEqual(result, {"username": "test", "password": "test123"})
        mock_client.get_secret_value.assert_called_once_with(SecretId="test-secret")
    
    @patch('boto3.session.Session')
    def test_get_secret_client_error(self, mock_session):
        """Test secret retrieval with client error"""
        from botocore.exceptions import ClientError
        
        mock_client = Mock()
        mock_session.return_value.client.return_value = mock_client
        mock_client.get_secret_value.side_effect = ClientError(
            {'Error': {'Code': 'ResourceNotFoundException'}}, 'GetSecretValue'
        )
        
        secrets_manager = SecretsManager()
        
        with self.assertRaises(EventComboETLError):
            secrets_manager.get_secret("nonexistent-secret")


class TestEventComboAPI(unittest.TestCase):
    """Test EventComboAPI functionality"""
    
    def setUp(self):
        self.api = EventComboAPI()
    
    @patch('requests.Session.post')
    def test_authenticate_success(self, mock_post):
        """Test successful authentication"""
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"access_token": "test-token"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        result = self.api.authenticate("test@example.com", "password123")
        
        self.assertTrue(result)
        self.assertEqual(self.api.access_token, "test-token")
        self.assertIn("Authorization", self.api.session.headers)
    
    @patch('requests.Session.post')
    def test_authenticate_failure(self, mock_post):
        """Test authentication failure"""
        import requests
        mock_response = Mock()
        mock_response.raise_for_status.side_effect = requests.exceptions.RequestException("Auth failed")
        mock_post.return_value = mock_response
        
        with self.assertRaises(EventComboETLError):
            self.api.authenticate("test@example.com", "wrong-password")
    
    @patch('requests.Session.get')
    def test_get_event_list_success(self, mock_get):
        """Test successful event list retrieval"""
        self.api.access_token = "test-token"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"events": [{"id": 1, "name": "Test Event"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        result = self.api.get_event_list()
        
        self.assertEqual(result, {"events": [{"id": 1, "name": "Test Event"}]})
    
    def test_get_event_list_not_authenticated(self):
        """Test event list retrieval without authentication"""
        with self.assertRaises(EventComboETLError):
            self.api.get_event_list()


class TestS3Uploader(unittest.TestCase):
    """Test S3Uploader functionality"""
    
    @patch('boto3.client')
    def test_upload_json_data_success(self, mock_boto_client):
        """Test successful S3 upload"""
        mock_s3_client = Mock()
        mock_boto_client.return_value = mock_s3_client
        
        uploader = S3Uploader("test-bucket")
        test_data = {"test": "data"}
        
        result = uploader.upload_json_data(test_data, "test/key.json")
        
        self.assertTrue(result)
        mock_s3_client.put_object.assert_called_once()


class TestRetryHandler(unittest.TestCase):
    """Test RetryHandler functionality"""
    
    def test_retry_success_first_attempt(self):
        """Test successful execution on first attempt"""
        mock_func = Mock(return_value="success")
        
        result = RetryHandler.retry_with_backoff(mock_func, max_retries=3)
        
        self.assertEqual(result, "success")
        mock_func.assert_called_once()
    
    def test_retry_success_after_failures(self):
        """Test successful execution after some failures"""
        mock_func = Mock(side_effect=[Exception("fail"), Exception("fail"), "success"])
        
        result = RetryHandler.retry_with_backoff(mock_func, max_retries=3, base_delay=0.01)
        
        self.assertEqual(result, "success")
        self.assertEqual(mock_func.call_count, 3)
    
    def test_retry_max_retries_exceeded(self):
        """Test failure after max retries exceeded"""
        mock_func = Mock(side_effect=Exception("always fail"))
        
        with self.assertRaises(EventComboETLError):
            RetryHandler.retry_with_backoff(mock_func, max_retries=2, base_delay=0.01)


class TestEventComboETL(unittest.TestCase):
    """Test main ETL orchestrator"""
    
    def setUp(self):
        self.config = {
            'secret_name': 'test-secret',
            's3_bucket': 'test-bucket',
            's3_key_prefix': 'test/prefix',
            'aws_region': 'us-west-2',
            'eventcombo_base_url': 'https://test.eventcombo.com',
            'max_retries': 2,
        }
    
    @patch('eventcombo_etl_improved.SecretsManager')
    @patch('eventcombo_etl_improved.EventComboAPI')
    @patch('eventcombo_etl_improved.S3Uploader')
    def test_run_success(self, mock_s3_uploader, mock_api, mock_secrets_manager):
        """Test successful ETL run"""
        # Mock secrets manager
        mock_secrets_instance = Mock()
        mock_secrets_manager.return_value = mock_secrets_instance
        mock_secrets_instance.get_secret.return_value = {
            'username': 'test@example.com',
            'password': 'password123'
        }
        
        # Mock API
        mock_api_instance = Mock()
        mock_api.return_value = mock_api_instance
        mock_api_instance.authenticate.return_value = True
        mock_api_instance.get_event_list.return_value = {"events": []}
        
        # Mock S3 uploader
        mock_s3_instance = Mock()
        mock_s3_uploader.return_value = mock_s3_instance
        mock_s3_instance.upload_json_data.return_value = True
        
        etl = EventComboETL(self.config)
        result = etl.run()
        
        self.assertTrue(result)
        mock_api_instance.authenticate.assert_called_once()
        mock_api_instance.get_event_list.assert_called_once()
        mock_s3_instance.upload_json_data.assert_called_once()


def run_security_checks():
    """Run basic security checks on the improved code"""
    print("🔒 Running security checks...")
    
    # Check for hardcoded credentials
    with open('eventcombo_etl_improved.py', 'r') as f:
        content = f.read()
        
        # Check for common credential patterns
        security_issues = []
        
        if 'password' in content.lower() and '=' in content:
            # Look for password assignments (excluding variable names and comments)
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if 'password' in line.lower() and '=' in line and not line.strip().startswith('#'):
                    # Exclude legitimate uses like dictionary keys, variable names, etc.
                    if ('secret_data[' not in line and 'credentials[' not in line and 
                        'required_keys' not in line and '[' not in line and 
                        'password"' not in line and "'password'" not in line):
                        security_issues.append(f"Line {i}: Potential hardcoded password")
        
        if 'username' in content.lower() and '@' in content and '=' in content:
            lines = content.split('\n')
            for i, line in enumerate(lines, 1):
                if '@' in line and '=' in line and not line.strip().startswith('#'):
                    if 'secret_data[' not in line and 'credentials[' not in line:
                        security_issues.append(f"Line {i}: Potential hardcoded username")
        
        if security_issues:
            print("❌ Security issues found:")
            for issue in security_issues:
                print(f"  - {issue}")
        else:
            print("✅ No obvious security issues found")
    
    print("✅ Security checks completed")


if __name__ == "__main__":
    print("🧪 Running EventCombo ETL tests...")
    
    # Run unit tests
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run security checks
    run_security_checks()
    
    print("✅ All tests completed")