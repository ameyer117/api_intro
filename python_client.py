import requests
from datetime import datetime
import uuid
import random

# Note to run this you must install the requests library via a virtual environment (For example)
# python3 -m venv .venv
# source .venv/bin/activate
# pip install requests

# Base URL of the API
BASE_URL = 'https://api-intro-app-vhrnt.ondigitalocean.app'

def create_user(email: str, full_name: str, password: str):
    """
    Create a new user.
    """
    url = f'{BASE_URL}/users/'
    data = {
        'email': email,
        'full_name': full_name,
        'password': password
    }

    # You can use verify=False to ignore SSL certificate issues such as self-signed certificates
    response = requests.post(url, json=data, verify=False)
    if response.status_code == 200:
        print('User created successfully.')
    else:
        print('Failed to create user:', response.json())
    return response

def login(email, password):
    """
    Log in to get an access token.
    """
    url = f'{BASE_URL}/users/token'
    data = {
        'email': email,
        'password': password
    }
    response = requests.post(url, json=data)
    if response.status_code == 200:
        token = response.json()['access_token']
        if token:
            print('Logged in successfully.')
        else:
            raise Exception('No access token found in response:', response.json())
        return token
    else:
        print('Failed to log in:', response.json())
        return None

def get_current_user(token: str):
    """
    Retrieve information about the current user.
    """
    url = f'{BASE_URL}/users/me'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    print('Current user info:', response.json())

def create_cve(token, cve_id, description, severity, published_date):
    """
    Create a new CVE entry.
    """
    url = f'{BASE_URL}/cves/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        'cve_id': cve_id,
        'description': description,
        'severity': severity,
        'published_date': published_date
    }
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 201:
        print('CVE created successfully:', response.json())
    else:
        print('Failed to create CVE:', response.json())
    return response

def get_cves(token, skip=0, limit=100):
    """
    Retrieve a list of CVEs.
    """
    url = f'{BASE_URL}/cves/'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    params = {
        'skip': skip,
        'limit': limit
    }
    response = requests.get(url, headers=headers, params=params)
    print('List of CVEs:', response.json())

def get_cve(token, cve_id):
    """
    Retrieve a specific CVE by ID.
    """
    url = f'{BASE_URL}/cves/{cve_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        print('CVE details:', response.json())
    else:
        print('Failed to retrieve CVE:', response.json())

def update_cve(token, cve_id, update_data):
    """
    Update an existing CVE.
    """
    url = f'{BASE_URL}/cves/{cve_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.put(url, json=update_data, headers=headers)
    if response.status_code == 200:
        print('CVE updated successfully:', response.json())
    else:
        print('Failed to update CVE:', response.json())

def delete_cve(token, cve_id):
    """
    Delete a CVE by ID.
    """
    url = f'{BASE_URL}/cves/{cve_id}'
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.delete(url, headers=headers)
    if response.status_code == 200:
        print('CVE deleted successfully.')
    else:
        print('Failed to delete CVE:', response.json())

def main():
    # Generate a unique email to avoid conflicts
    unique_id = uuid.uuid4().hex
    email = f'user_{unique_id}@example.com'
    full_name = 'Test User'
    password = 'password123'

    # Step 1: Create a new user
    create_user(email, full_name, password)

    # Step 2: Log in to get an access token
    token = login(email, password)

    # Step 3: Retrieve current user info
    get_current_user(token)

    # Step 4: Create a new CVE entry
    # Generate a unique CVE ID with 5 random numbers
    random_part = ""
    for _ in range(5):
        random_part += str(random.randint(0, 9))

    cve_id = f'CVE-2023-{random_part}'
    description = 'This is a test CVE entry.'
    severity = 'HIGH'  # Options: CRITICAL, HIGH, MODERATE, LOW
    published_date = datetime.utcnow().isoformat() + 'Z'
    create_cve(token, cve_id, description, severity, published_date)

    # Step 5: Retrieve the list of CVEs
    get_cves(token)

    # Step 6: Retrieve the specific CVE just created
    get_cve(token, cve_id)

    # Step 7: Update the CVE entry
    print(f"Updating the CVE entry {cve_id}")
    update_data = {
        'cve_id': cve_id,
        'description': 'Updated CVE description.',
        'severity': 'CRITICAL'
    }
    update_cve(token, cve_id, update_data)

    # Step 8: Delete the CVE entry
    delete_cve(token, cve_id)

if __name__ == '__main__':
    main()
