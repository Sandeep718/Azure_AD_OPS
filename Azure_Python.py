import msal
import requests

TENANT_ID = "y195e8969-c853-47b4-83d0-36e044d83923"
CLIENT_ID = "e2e46ae3-2dee-4eed-a074-ddffd760ab2b"
CLIENT_SECRET = "790fcd50-0720-4572-9f6c-f60d4d219ede"

AUTHORITY = f"https://login.microsoftonline.com/{TENANT_ID}"
GRAPH_API_ENDPOINT = "https://graph.microsoft.com/v1.0"

# Authenticate with Azure AD
def get_access_token():
    app = msal.ConfidentialClientApplication(CLIENT_ID, CLIENT_SECRET, AUTHORITY)
    token = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    return token["access_token"]

# Check if a user exists
def check_user(user_principal_name):
    token = get_access_token()
    url = f"{GRAPH_API_ENDPOINT}/users/{user_principal_name}"
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(url, headers=headers)
    return response.status_code == 200

# Enable or disable user account
def set_account_status(user_id, enable=True):
    token = get_access_token()
    url = f"{GRAPH_API_ENDPOINT}/users/{user_id}"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"accountEnabled": enable}
    response = requests.patch(url, headers=headers, json=data)
    return response.status_code == 204

# Change group assignment
def change_group_assignment(user_id, group_id, action="add"):
    token = get_access_token()
    url = f"{GRAPH_API_ENDPOINT}/groups/{group_id}/members/$ref"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    data = {"@odata.id": f"{GRAPH_API_ENDPOINT}/directoryObjects/{user_id}"}
    if action == "add":
        response = requests.post(url, headers=headers, json=data)
    else:
        response = requests.delete(url, headers=headers)
    return response.status_code in [204, 201]

# Create a new user
def create_user(user_details):
    token = get_access_token()
    url = f"{GRAPH_API_ENDPOINT}/users"
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=user_details)
    return response.status_code in [200, 201]
check_user(Abhishek.U@amitomar63gmail.onmicrosoft.com)
