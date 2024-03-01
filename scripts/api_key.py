import requests

headers = {
    'Content-Type': 'application/json',
}

json_data = {
    'name': 'test',
    'role': 'Admin',
}

response = requests.post('http://localhost:3000/api/serviceaccounts', headers=headers, json=json_data, auth=('admin', 'admin'))
account_id = response.json()["id"]

json_data = {
    'name': 'test-token',
}
response = requests.post(
    f"http://localhost:3000/api/serviceaccounts/{account_id}/tokens",
    headers=headers,
    json=json_data,
    auth=('admin', 'admin'),
)
GRAFANA_KEY = response.json()["key"]  # to be saved in environment variables
