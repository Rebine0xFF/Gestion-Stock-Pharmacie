import requests

url = "http://192.168.0.11:80/insert_db_item"
data = {
    "name": "NEWITEMWOW",
    "batch_number": "BBBBBQQQ",
    "initial_quantity": 90,
    "expiration_date": "2025-09-10",
    "form": "Comprimé",
    "dosage": "500mg",
    "prescription_required": True
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Text:", response.text)