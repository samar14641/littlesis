# testing APIs and results, along with storage

import requests
from pprint import pprint

baseURL = 'https://littlesis.org/api/'

# /entities/:id?details=TRUE
entID = str(1)
params = {'details': 'TRUE'}

resp = requests.get(baseURL + 'entities/' + entID, params = params)
data = resp.json()

print(resp.url, resp.status_code)
# pprint(data)
print(data['data']['attributes']['name'])