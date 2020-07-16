import json
import os
import pickle
import requests
import time
# from pprint import pprint
from sys import exit

minSleep = 0.5

def relInit():
    relID = 1

    with open(os.getcwd() + '/Pickle/relID.pickle', 'wb') as pckl:
        pickle.dump(relID, pckl, pickle.HIGHEST_PROTOCOL)

def collector():
    startTime = time.time()

    relID = None  # relationship ID
    count = 0  # count of relationships collected
    maxCollect = 1696780  # max number of relationships to collect, as of 2020-07-16T11:40 there are 1,696,780 relationships
    baseURL = 'https://littlesis.org/api/relationships/'

    data = {}
    excpt = set()  # to log exceptions
    notOk = set()  # to log HTTP errors

    currentFile = 1

    with open(os.getcwd() + '/Pickle/relID.pickle', 'rb') as pckl:
        relID = pickle.load(pckl)  # load relID to start from

    if relID is None:
        print('relationship ID is None, aborting')
        exit(1)

    print('Starting from', relID)

    while count <= maxCollect - 1:
        try:
            resp = requests.get(baseURL + str(relID))
            t1 = time.time()
            
            if resp.status_code == 200:
                d = resp.json()['data']['attributes']
                data[d['id']] = d
                count += 1
                print(count, relID)

            else:  # some HTTP error i.e. status NOT 200
                print(relID, 'NOT OK', resp.status_code)
                notOk.add((relID, resp.status_code))  # log relID and resp code

        except Exception as e:
            print(relID, e)
            excpt.add(relID)  # log relID
            continue

        relID += 1

        if count % 500 == 0 and data:  # write after every 500 relationships
            with open(os.getcwd() + '/Data/relationship/relationship' + str(currentFile) + '.json', 'w', encoding = 'utf-8')  as f:
                json.dump(data, f, ensure_ascii = False, indent = 4)   

            data = {} 

            print('written relationship' + str(currentFile))

            currentFile += 1
        
        if count % 500 == 0 and len(notOk) > 0:  # write notOk log if any
            with open(os.getcwd() + '/Pickle/notOk/relationship_notOk' + str(currentFile - 1) + '.pickle', 'wb') as pckl:
                pickle.dump(notOk, pckl, pickle.HIGHEST_PROTOCOL)

            notOk = set()

            print('written relationship_notOk' + str(currentFile - 1))

        t2 = time.time()

        if t2 - t1 < minSleep:
            time.sleep(minSleep - (t2 - t1))  

        if relID == 1696781:
            break 

    # pprint(notOk)  

    if data:  # write remaining data if any
        with open(os.getcwd() + '/Data/relationship/relationship' + str(currentFile) + '.json', 'w', encoding = 'utf-8')  as f:
            json.dump(data, f, ensure_ascii = False, indent = 4)  

        print('written relationship' + str(currentFile))
        
    if notOk:  # write remaining notOk logs if any
        with open(os.getcwd() + '/Pickle/notOk/relationship_notOk' + str(currentFile) + '.pickle', 'wb') as pckl:
            pickle.dump(notOk, pckl, pickle.HIGHEST_PROTOCOL)

        print('written relationship_notOk' + str(currentFile))

    endTime = time.time()
    print('Time taken (min):', (endTime - startTime) / 60)
    print('Count:', count)

relInit()
collector()