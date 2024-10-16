import requests

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

# Output email templates data
print(email_templates)
