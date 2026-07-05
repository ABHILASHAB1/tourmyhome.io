import urllib.request
import json

try:
    req = urllib.request.Request("http://localhost:8000/")
    with urllib.request.urlopen(req) as response:
        print("Root /:", response.read().decode())
except Exception as e:
    print("Root / Error:", e)

try:
    req = urllib.request.Request("http://localhost:8000/api/v1/listings/")
    with urllib.request.urlopen(req) as response:
        print("Listings /:", response.read().decode()[:100])
except Exception as e:
    print("Listings / Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())

try:
    data = b"username=admin%40souqai.com&password=password123"
    req = urllib.request.Request("http://localhost:8000/api/v1/auth/login", data=data)
    with urllib.request.urlopen(req) as response:
        print("Login /:", response.read().decode())
except Exception as e:
    print("Login / Error:", e)
    if hasattr(e, 'read'):
        print(e.read().decode())
