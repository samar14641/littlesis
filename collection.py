import json
import os
import pickle
import requests
import time
from pprint import pprint
from sys import exit

minSleep = 0.5

def simpleIterativeCollect():
    entID = 1  # entity ID
    count = 0
    maxCollect = 100
    baseURL = 'https://littlesis.org/api/entities/'
    params = {'details': 'TRUE'}

    data = {}

    while count <= maxCollect - 1:
        try:
            resp = requests.get(baseURL + str(entID), params = params)
            t1 = time.time()
            
            if resp.status_code == 200:
                d = resp.json()['data']['attributes']
                data[d['name']] = d
                count += 1
                print(count)

            else: 
                print(entID, 'NOT OK', resp.status_code)
                # log this entID somewhere

        except Exception as e:
            print(entID, e)
            # log this entID somewhere
            continue

        entID += 1

        t2 = time.time()

        if t2 - t1 < minSleep:
            time.sleep(minSleep - (t2 - t1))    

    # pprint(data)    

    with open(os.getcwd() + '\\Data\\collect150.json', 'w', encoding = 'utf-8')  as f:
        json.dump(data, f, ensure_ascii = False, indent = 4)

def collectorInit():
    entID = 1

    with open(os.getcwd() + '\\Pickle\\entID.pickle', 'wb') as pckl:
        pickle.dump(entID, pckl, pickle.HIGHEST_PROTOCOL)

def collector():
    startTime = time.time()

    entID = None  # entity ID
    count = 0
    maxCollect = 1000
    baseURL = 'https://littlesis.org/api/entities/'
    params = {'details': 'TRUE'}

    data = {}
    excpt = set()
    notOk = set()

    currentFile = 1

    with open(os.getcwd() + '\\Pickle\\entID.pickle', 'rb') as pckl:
        entID = pickle.load(pckl)

    if entID is None:
        print('entity ID is None, aborting')
        exit(1)

    print('Starting from', entID)

    while count <= maxCollect - 1:
        try:
            resp = requests.get(baseURL + str(entID), params = params)
            t1 = time.time()
            
            if resp.status_code == 200:
                d = resp.json()['data']['attributes']
                data[d['name']] = d
                count += 1
                print(count, entID)

            else: 
                print(entID, 'NOT OK', resp.status_code)
                notOk.add((entID, resp.status_code))  # log entID and resp code

        except Exception as e:
            print(entID, e)
            excpt.add(entID)  # log entID
            continue

        entID += 1

        if count % 100 == 0 and data:  # write after every 100 entities
            with open(os.getcwd() + '\\Data\\entity' + str(currentFile) + '.json', 'w', encoding = 'utf-8')  as f:
                json.dump(data, f, ensure_ascii = False, indent = 4)   

            print('written e' + str(currentFile))
            currentFile += 1

            data = {} 

        t2 = time.time()

        if t2 - t1 < minSleep:
            time.sleep(minSleep - (t2 - t1))    

    # pprint(notOk)       
    with open(os.getcwd() + '\\Pickle\\notOk.pickle', 'wb') as pckl:
        pickle.dump(notOk, pckl, pickle.HIGHEST_PROTOCOL)

    # TO DO:
    # -> data logger outside loop for final round of data
    # -> notOk logger in loop if notOk is not {} every 1000 iters, use currentFile counter

    endTime = time.time()
    print('Time taken (min):', (endTime - startTime) / 60)
    print('Count:', count)

# simpleIterativeCollect()
# collectorInit()
collector()