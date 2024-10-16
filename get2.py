import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.ssl_ import create_urllib3_context

class TLSAdapter(HTTPAdapter):
    def init_poolmanager(self, *args, **kwargs):
        context = create_urllib3_context()
        context.options |= 0x4  # OP_NO_SSLv3 (Disable SSLv3)
        kwargs['ssl_context'] = context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

session = requests.Session()
session.mount('https://', TLSAdapter())

auth_url = 'https://YOUR_SUBDOMAIN.auth.marketingcloudapis.com/v2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'account_id': 'YOUR_ACCOUNT_ID'
}

response = session.post(auth_url, json=auth_data)
print(response.json())


import httpx

auth_url = 'https://YOUR_SUBDOMAIN.auth.marketingcloudapis.com/v2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'account_id': 'YOUR_ACCOUNT_ID'
}

with httpx.Client() as client:
    response = client.post(auth_url, json=auth_data)
    print(response.json())



import requests
import ssl
from urllib3.poolmanager import PoolManager
from requests.adapters import HTTPAdapter

class TLSAdapter(HTTPAdapter):
    """Transport adapter that forces TLSv1.2"""
    def init_poolmanager(self, *args, **kwargs):
        context = ssl.create_default_context()
        context.minimum_version = ssl.TLSVersion.TLSv1_2
        kwargs['ssl_context'] = context
        return super(TLSAdapter, self).init_poolmanager(*args, **kwargs)

# Create a session with the adapter
session = requests.Session()
session.mount('https://', TLSAdapter())

auth_url = 'https://YOUR_SUBDOMAIN.auth.marketingcloudapis.com/v2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'account_id': 'YOUR_ACCOUNT_ID'
}

try:
    response = session.post(auth_url, json=auth_data, timeout=30)
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")



import requests

auth_url = 'https://YOUR_SUBDOMAIN.auth.marketingcloudapis.com/v2/token'
auth_data = {
    'grant_type': 'client_credentials',
    'client_id': 'YOUR_CLIENT_ID',
    'client_secret': 'YOUR_CLIENT_SECRET',
    'account_id': 'YOUR_ACCOUNT_ID'
}

try:
    # Disable SSL verification
    response = requests.post(auth_url, json=auth_data, verify=False, timeout=30)
    response.raise_for_status()  # Raise an error for bad status codes
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"Error: {e}")
