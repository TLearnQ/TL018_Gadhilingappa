import requests, json

TOKEN = " Bearer reqres-token"

headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/json"
}

url = "https://reqres.in/api/users/2"

payload = {
    "job": "oracle",
    "name": "ram"
}

# res = requests.put(url, data=payload)
res = requests.put(url, data=payload, headers=headers)
print("Status code: ", res.status_code)
print("Response:",res.json())



