import requests
import keyboard


keyboard.wait("p")




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




keyboard.wait("p")




url = "http://192.168.0.11:80/subtract_db_item"
data = {
    "batch_number": "A98765"
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Text:", response.text)




keyboard.wait("p")





url = "http://192.168.0.11:80/remove_db_item"
data = {
    "batch_number": "BBBBBQQQ"
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Text:", response.text)