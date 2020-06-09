# testing APIs and results, along with storage
# TO DO: find the min sleep time, currently set to 0.5

import requests
import time
from pprint import pprint

minSleep = 0.5

def basicRequests():
    baseURL = 'https://littlesis.org/api/'
    entID = str(1)
    relID = str(1)

    # /entities/:id?details=TRUE
    params = {'details': 'TRUE'}

    resp = requests.get(baseURL + 'entities/' + entID, params = params)
    data = resp.json()

    print(resp.url, resp.status_code)
    # pprint(data)
    print(data['data']['attributes']['name'])
    time.sleep(minSleep)   


    # /entities/:id/extensions
    resp = requests.get(baseURL + 'entities/' + entID + '/extensions')
    data = resp.json()

    print(resp.url, resp.status_code)
    pprint(data['data'][0])
    time.sleep(minSleep)


    # /entities/:id/relationships
    resp = requests.get(baseURL + 'entities/' + entID + '/relationships')
    data = resp.json()

    print(resp.url, resp.status_code)
    print(data['data'][0]['attributes']['description'])
    time.sleep(minSleep)


    # /entities/:id/connections
    resp = requests.get(baseURL + 'entities/' + entID + '/connections')
    data = resp.json()

    print(resp.url, resp.status_code)
    print(data['data'][0]['attributes']['name'])
    time.sleep(minSleep)


    # /entities/:id/lists
    resp = requests.get(baseURL + 'entities/' + entID + '/lists')
    data = resp.json()

    print(resp.url, resp.status_code)
    print(data['data'][0]['attributes']['description'])
    time.sleep(minSleep)


    # /entities/search?q=name
    params = {'q': 'Bill Gates'}

    resp = requests.get(baseURL + 'entities/search', params = params)
    data = resp.json()

    print(resp.url, resp.status_code)
    print(data['data'][0]['attributes']['name'])
    time.sleep(minSleep)


    # /relationships/:id
    resp = requests.get(baseURL + 'relationships/' + relID)
    data = resp.json()

    print(resp.url, resp.status_code)
    print(data['data']['attributes']['description'])


basicRequests()