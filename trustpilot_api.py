import requests
import base64

# Step 1: Obtain the access token
api_key = 'YOUR_API_KEY'
api_secret = 'YOUR_API_SECRET'
credentials = f"{api_key}:{api_secret}"
encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')

token_url = "https://api.trustpilot.com/v1/oauth/oauth-business-users-for-applications/accesstoken"
token_headers = {
    "Authorization": f"Basic {encoded_credentials}",
    "Content-Type": "application/x-www-form-urlencoded"
}
token_data = {
    "grant_type": "client_credentials"
}

token_response = requests.post(token_url, headers=token_headers, data=token_data)
token_response.raise_for_status()
access_token = token_response.json().get("access_token")

# Step 2: Generate the invitation link
business_unit_id = "YOUR_BUSINESS_UNIT_ID"
invitation_url = f"https://invitations-api.trustpilot.com/v1/private/business-units/{business_unit_id}/invitation-links"
invitation_headers = {
    "Authorization": f"Bearer {access_token}",
    "Content-Type": "application/json"
}
invitation_data = {
    "locationId": "ABC123",
    "referenceId": "inv00001",
    "email": "john.doe@trustpilot.com",
    "name": "John Doe",
    "locale": "en-US",
    "tags": ["tag1", "tag2"],
    "redirectUri": "http://trustpilot.com"
}

invitation_response = requests.post(invitation_url, headers=invitation_headers, json=invitation_data)
invitation_response.raise_for_status()
invitation_link = invitation_response.json().get("url")

print(f"Generated Invitation Link: {invitation_link}")
