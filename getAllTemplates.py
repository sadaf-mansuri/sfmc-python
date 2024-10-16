import requests
import json
import os

# Step 1: Get OAuth token
auth_url = 'https://YOUR_SUBDOMAIN.auth.marketingcloudapis.com/v2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'account_id': 'YOUR_ACCOUNT_ID'
}
auth_response = requests.post(auth_url, json=auth_data)
auth_response_data = auth_response.json()
access_token = auth_response_data['access_token']

# Step 2: Get email templates with pagination
api_url = 'https://YOUR_SUBDOMAIN.rest.marketingcloudapis.com/asset/v1/content/assets'
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
params = {
    '$filter': 'assetType.id+eq+207',  # filter for email templates
    'page': 1,  # Page number
    'pageSize': 10  # Page size
}
response = requests.get(api_url, headers=headers, params=params)
email_templates = response.json()

# Step 3: Parse the JSON and save HTML templates to files
for item in email_templates['items']:
    file_name = item['fileProperties']['fileName'] if 'fileProperties' in item else f'template_{item["id"]}.html'
    html_content = item['views']['html']['content'] if 'views' in item and 'html' in item['views'] else ''
    
    # Save the HTML content to a file
    with open(file_name, 'w', encoding='utf-8') as file:
        file.write(html_content)

    print(f"Saved template {item['name']} as {file_name}")
