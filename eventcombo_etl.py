import os
import sys
import json
import time
import random
import requests
import boto3
from datetime import datetime, timedelta
from botocore.exceptions import ClientError

# ----------- Secrets Manager -----------
def get_secret():
    secret_name = "eventcombo"
    region_name = "us-west-2"
    session = boto3.session.Session()
    client = session.client(service_name='secretsmanager', region_name=region_name)

    try:
        response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        raise e

    return json.loads(response['SecretString'], strict=False)

# ----------- Auth Token -----------
def get_access_token():

    #secret_dict = get_secret()
    #username = secret_dict["username"]
	#password = secret_dict["password"]
    username = "classes.events@sharp.com"
    password = "Sharphealthcare2025!" 
    
	# Define the API endpoint for token
    url = "https://www.eventcombo.com/API/Token"
    
    # Define the payload for password grant type
    payload = {
        "grant_type": "password",
        "username": username,
        "password": password
    }
    
    # Set up the headers
    headers = {
        "accept": "application/json",
        "content-type": "application/x-www-form-urlencoded;charset=UTF-8"
    }
    
    try:
        # Make the request
        response = requests.post(url, data=payload, headers=headers)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse the JSON response
            token_data = response.json()
            access_token = token_data["access_token"]
            print("Authentication successful!")
            return access_token
        else:
            print(f"Authentication failed with status code: {response.status_code}")
            print(f"Error message: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
        return None

# ----------- Retry Wrapper -----------
def retry_request(func, *args, max_retries=5, delay=5):
    for attempt in range(max_retries):
        try:
            return func(*args)
        except requests.exceptions.RequestException as e:
            print(f"[Attempt {attempt+1}] Request failed: {e}")
            time.sleep(delay * (2 ** attempt) + random.uniform(0, 1))
    raise Exception("Max retries exceeded.")

# ----------- S3 Upload -----------
def upload_to_s3(response_body, filename):
    bucket_name = "shc-ea-fivetran"
    json_file = f"{filename}.json"
    s3_key = f"fivetran/eventcombo/{json_file}"

    with open(json_file, 'w') as file:
        json.dump(response_body, file)
        print(f"✅ Data written to {json_file}")

    s3 = boto3.client('s3')
    try:
        with open(json_file, 'rb') as file:
            s3.put_object(Body=file, Bucket=bucket_name, Key=s3_key)
            print(f"✅ Uploaded to S3: {s3_key}")
    except Exception as e:
        print("❌ S3 Upload Failed:", e)

# ----------- EventCombo API Calls -----------
def download_eventlist():
    print('in exec_report function')
    access_token = get_access_token()
    #now_utc = datetime.utcnow()
    #from_time = (now_utc - timedelta(hours=6)).strftime("%Y-%m-%dT%H:%M:%SZ")
    #to_time = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")

    url = f"https://www.eventcombo.com/api/v2/Public/Event/List"
    payload = {}
    headers = {
		"Authorization": f"Bearer {access_token}"
	}

    response = requests.request("GET", url, headers=headers, data=payload)
    response.raise_for_status()
    return response.json()

# ----------- Orchestration -----------
def call_api():
    print(f"🚀 Executing report")
    data = retry_request(download_eventlist)
    upload_to_s3(data, 'eventlist')

# ----------- Main -----------
def main():
    print("🟢 Starting EventCombo ETL job...")
    call_api()
    print("✅ Job completed.")

if __name__ == "__main__":
    main()