import urllib.request
import json

try:
    req = urllib.request.Request("http://localhost:8000/api/v1/listings/")
    with urllib.request.urlopen(req) as response:
        data = json.loads(response.read().decode())
        print("Success! Data type:", type(data))
        if isinstance(data, dict):
            print("Data dict keys:", data.keys())
        elif isinstance(data, list):
            print("Data list length:", len(data))
except urllib.error.HTTPError as e:
    print(f"HTTPError: {e.code}")
    print(e.read().decode())
except Exception as e:
    print(f"Error: {e}")
