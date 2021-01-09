import http.client
import json
# import pandas as pd
# from pandas import DataFrame
import tkinter as tk
from tkinter import filedialog
import csv

# Set to 1 to show details along the way for debugging purposes
debug=0

previousCSV = filedialog.askopenfilename()

def getDataFromAPI():
    # connect to instagram api
    conn = http.client.HTTPSConnection("instagramdimashirokovv1.p.rapidapi.com")

    # user id for flyingfrugalwithrosie
    username_id = "37836191304"

    headers = {
        'x-rapidapi-host': "InstagramdimashirokovV1.p.rapidapi.com",
        'x-rapidapi-key': "a6b66d4772msh310698cfe8ec298p1019fajsn63a985543ccc",
        'userid': username_id,
        'cursor': "optional"
        }
    conn.request("GET", "/followers/5821462185/optional?cursor=optional&userid=5821462185", headers=headers)

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))

    return json.loads(data.decode("utf-8"))

def getPreviousFollowers(file_name):
    with open(file_name, mode='r') as csv_file:
        csv_reader = csv.DictReader(csv_file)
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                print(f'Column names are {", ".join(row)}')
                line_count += 1
            print(f'\t{row["id"]} has username {row["username"]}')
            line_count += 1
        print(f'Processed {line_count} lines.')
        return csv_reader

def getPreviousIds(file_name):
    previous_ids = list()
    with open(file_name) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 1
    line = 0
    for row in csv_reader:
        if line == 0:
            line += 1
        else:
            previous_ids.append(row[0])
    return previous_ids



#recieves two dictionaries, dictionaries should have id first
def insertFollowers(newFollowers, oldFollowers):
    i = 0
    for follower_id in newFollowers['id']:
        #binary serach to find follower  
        low = 0
        high = len(oldFollowers['id']) -1
        mid = 0
        while low <= high:
            mid = (high + low) //2
            if oldFollowers['id'][mid] < follower_id:
                low = mid + 1
            elif oldFollowers['id'][mid] > follower_id:
                high = mid - 1
            else:
                mid = -1
                break

        if mid == -1:
            pass
        else:
            if oldFollowers['id'][mid] < follower_id:
                oldFollowers['id'].insert(mid+1, follower_id)
                oldFollowers['username'].insert(mid+1, newFollowers['username'][i])
            else:
                oldFollowers['id'].insert(mid, follower_id)
                oldFollowers['username'].insert(mid, newFollowers['username'][i])
        i += 1
    return oldFollowers


def jsonToDictData(json_dictionary):
    follower_usernames = list()
    follower_ids = []
    i = 0

    print(json_dictionary)

    previous_ids = getPreviousIds()

    for item in json_dictionary['edges']:
        id = item['node']['id']
        follower_usernames.append(item['node']['username'])
        follower_ids.append(item['node']['id'])

    follower_data = {"ids": follower_ids,
        "usernames": follower_usernames}
    
    return follower_data



def exportCSV(x):
    export_file_path = 'followers_data.csv'
    x.to_csv(export_file_path, index=True, header=True)


d = insertFollowers({'id' : [2, 124, 5, 23423, 23234, 8, 12],
                    'username': ['otherphil', 'hasdf', 'phil', 'tdude', 'asdf', 'dude', 'hello']}, {'id' : [5, 8, 12, 23234],
                    'username': [ 'phil', 'asdf', 'dude', 'tdude']})
print(d)