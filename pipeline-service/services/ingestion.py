import requests

FLASK_URL = "http://mock-server:5000/api/customers"

def fetch_all_data():
    page = 1
    all_data = []

    while True:
        res = requests.get(FLASK_URL, params={"page": page, "limit": 10})
        data = res.json()

        all_data.extend(data["data"])

        if len(data["data"]) < 10:
            break

        page += 1

    return all_data