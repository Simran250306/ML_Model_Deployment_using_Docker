import requests
from pprint import pprint

url = 'http://localhost:8000/predict'
headers = {
    'Origin': 'http://localhost:8001',
    'Access-Control-Request-Method': 'POST',
    'Access-Control-Request-Headers': 'content-type'
}

print('Sending OPTIONS preflight to', url)
try:
    r = requests.options(url, headers=headers, timeout=5)
except Exception as e:
    print('Request failed:', e)
else:
    print('Status:', r.status_code)
    print('\nResponse headers:')
    pprint(dict(r.headers))
    print('\nBody:')
    print(r.text)
