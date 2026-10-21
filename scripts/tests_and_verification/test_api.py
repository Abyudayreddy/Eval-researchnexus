import requests

try:
    r = requests.get("http://localhost:8000/api/papers/fced8220-c6e8-4d73-9434-9307aac7fb89/status")
    print(r.status_code)
    print(r.text)
except Exception as e:
    print(e)
