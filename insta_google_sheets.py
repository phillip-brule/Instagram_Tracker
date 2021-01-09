import http.client
import json
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import sys
import time
import auto_messenger


# Set to 1 to show details along the way for debugging purposes
debug=0

#returns json of all current followers
def getDataFromAPI(user_id, cursor):
    # connect to instagram api
    conn = http.client.HTTPSConnection("instagramdimashirokovv1.p.rapidapi.com")

    if cursor == None:
        cursor = "optional"
    
    headers = {
        'x-rapidapi-host': "InstagramdimashirokovV1.p.rapidapi.com",
        'x-rapidapi-key': "a6b66d4772msh310698cfe8ec298p1019fajsn63a985543ccc",
        'userid': user_id,
        'cursor': cursor
        }
    conn.request("GET", "/followers/"+user_id+"/"+cursor+"?cursor="+cursor+"&userid="+user_id, headers=headers)

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))
    json_dictionary = json.loads(data.decode("utf-8"))

    return json_dictionary

#returns the current google spread sheet
def getWorksheet():
    # define the scope
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']

    # add credentials to the account
    creds = ServiceAccountCredentials.from_json_keyfile_name('D:\Phill\Documents\Instagram_App\My First Project-f47b7ed37c7c.json', scope)

    # authorize the clientsheet 
    client = gspread.authorize(creds)

    # get the instance of the Spreadsheet
    sheet = client.open('Automatic Follower Tracker')

    # get the first sheet of the Spreadsheet
    sheet_instance = sheet.get_worksheet(0)

    return sheet_instance


#method takes O(nlogn) 
#takes list of all current followers and the current worksheet, then returns new followers
def updateFollowers(worksheet, current_followers):
    old_follower_id_list = worksheet.col_values(4)
    #sorting takes O(n)
    sorted_follower_id = sorted(current_followers['ids'])
    
    date = datetime.now()
    date_string = date.strftime("%d/%m/%Y")

    #for loop takes O(nlogn) - O(n) to iterate through and O(logn) to search in new list
    for id in old_follower_id_list:
        #binary serach to find follower  
        if(id) == 'Id':
            continue
        if(id) == '':
            continue
        low = 0
        high = len(sorted_follower_id) -1
        mid = 0
        while low <= high:
            mid = (high + low) //2
            if sorted_follower_id[mid] < id:
                low = mid + 1
            elif sorted_follower_id[mid] > id:
                high = mid - 1
            else:
                mid = -1
                break
        if mid == -1:
            #I am assuming find() takes at most O(n) time
            
            cell = worksheet.find(id, in_column=4)
            worksheet.update_cell(cell.row, 5, "User unfollowed on " + date_string)
            worksheet.update_cell(cell.row, 6, "TRUE")
        else:
            i = current_followers['ids'].index(id)
            del current_followers['ids'][i]
            del current_followers['usernames'][i]
            del current_followers['names'][i]
    return current_followers

#only to update spreadsheet that emma has already been using for the first time
def firstTimeUpdate(worksheet, current_followers):
    date = datetime.now()
    date_string = date.strftime("%d/%m/%Y")

    old_follower_username_list = worksheet.col_values(2)
    follower_usernames = current_followers['usernames']

    i = 1
    for user in old_follower_username_list:
        if i == 1:
            i += 1
            continue
        j = 0
        for current_username in follower_usernames:
            if(j % 25 == 0):
                time.sleep(100)
            if current_username == user:
                print(current_username)
                try:
                    name = current_followers['names'][j]
                except:
                    name = "unknown"
                try:
                    id = current_followers['ids'][j]
                except:
                    id = "unknown"
                worksheet.update_cell(i, 3, name)
                worksheet.update_cell(i, 4, id)
                worksheet.update_cell(i, 1, date_string)
            j += 1
        i += 1


#recieves dictionary of the new followers and the worksheet
def insertNewFollowers(newFollowers, worksheet):
    follower_id_list = newFollowers['ids']
    date = datetime.now()
    date_string = date.strftime("%d/%m/%Y")
    i = 0
    for id in follower_id_list:
        try:
            username = newFollowers['usernames'][i]
        except:
            username = "unknown"
        try:
            name = newFollowers['names'][i]
        except:
            name = "unknown"
        worksheet.append_row([date_string, username, name, id])
        i += 1
    return 

#takes instagram api json data and returns a dictionary of the current follower information
#algorithm recursively calls itself to at the next page of results to the current dictionary
def jsonToDictData(user_id, json_dictionary):
    follower_usernames = []
    follower_ids = []
    follower_names = []

    msg_check = list(json_dictionary.keys())[0]
    if msg_check == 'message':
        print("Sorry, instagram api can't be accessed anymore today. Try again tomorrow.")
        time.sleep(1)
        return None

    for item in json_dictionary['edges']:
        follower_usernames.append(item['node']['username'])
        follower_ids.append(item['node']['id'])
        follower_names.append(item['node']['full_name'])

    if json_dictionary["page_info"]["has_next_page"] == True:
        cursor = json_dictionary["page_info"]["end_cursor"]
        time.sleep(1)   #can only make one request per second
        next_json = getDataFromAPI(user_id, cursor)
        new_data = jsonToDictData(user_id, next_json)
        if new_data == None:
            print("Saving data for tomorrow")
            time.sleep(1)
            writeToCursor(cursor)
        else:
            follower_usernames.extend(new_data["usernames"])
            follower_ids.extend(new_data["ids"])
            follower_names.extend(new_data["names"])


    follower_data = {"ids": follower_ids,
        "usernames": follower_usernames,
        "names": follower_names}
    print("returning follower_data")

    return follower_data


def readCursor():
    f = open("D:\\Phill\\Documents\\Instagram_App\\cursor.txt", "r")
    cursor = f.read()
    f.close()
    return cursor

def writeToCursor(msg):
    f = open("D:\\Phill\\Documents\\Instagram_App\\cursor.txt", "w")
    f.write(msg)
    f.close
    return

def writeToFollowers(msg):
    f = open("D:\\Phill\\Documents\\Instagram_App\\followers.txt", "w")
    f.write(msg)
    f.close

def readFollowers():
    f = open("D:\\Phill\\Documents\\Instagram_App\\followers.txt", "r")
    followers_string = f.read()
    f.close()    
    followers_dictionary = json.loads(followers_string)
    return followers_dictionary


def hasBeenFollowing(days_before_messaging):
    worksheet = getWorksheet()
    dates = worksheet.col_values(1)
    current_date = datetime.now()
    
    for date in dates:
        try:   
            py_date = time.strptime(date, "%d/%m/%Y")
        except:
            continue
        difference = abs((current_date - py_date).days)
        if difference >= days_before_messaging:
            return True
        else:
            return False


def autoMessageUsers(username, password, message, days_before_messaging):
    username = "flyingfrugalwithrosie"
    password = "surragate pass"
    message = "Welcome Message"
    worksheet = getWorksheet()
    not_messeged_list = worksheet.col_values(6)
    user_list = []
    i = 1
    for value in not_messeged_list:
        if value == 'FALSE' & hasBeenFollowing(days_before_messaging):
            user = worksheet.cell(i, 2)
            user_list.append(user)
        i += 1
    users_not_messaged = auto_messenger.run(username , password, user_list, message)
    for user in user_list:
        cell = worksheet.find(user, in_column= 2)
        worksheet.update_cell(cell.row, 6, "TRUE")
    for user in users_not_messaged:
        cell = worksheet.find(user, in_column= 2)
        worksheet.update_cell(cell.row, 6, "FALSE")
    return



def run(user_id):
    #get data from instagram and if there is a cursor to a page, continue from that page and get previous follower data
    print("Getting data from your instagram ...")
    cursor = readCursor()
    writeToCursor("Empty") #cursor file is Empty but the cursor variable may have a cursor variable
    current_followers_dictionary = None
    if cursor == "Empty":
        current_followers_dictionary = jsonToDictData(user_id, getDataFromAPI(user_id, None))
    else:
        #add follower data from preivous runs to datas current followers
        current_followers_dictionary = readFollowers()
        new_data = jsonToDictData(user_id, getDataFromAPI(user_id, cursor))
        if new_data == None:
            writeToCursor(cursor)
            sys.exit(1)
        current_followers_dictionary["usernames"].extend(new_data["usernames"])
        current_followers_dictionary["ids"].extend(new_data["ids"])
        current_followers_dictionary["names"].extend(new_data["names"])

    #if there is a new cursor that means that not all the follower data was collected and needs to be continued at a later time
    cursor = readCursor()
    if cursor != "Empty":
        writeToFollowers(json.dumps(current_followers_dictionary))
        sys.exit(1)

    writeToFollowers("")

    #collecting data was successful. Time to update google spreadsheet
    worksheet = getWorksheet()
    print("Updating people who unfollowed you and finding your new followers ...")
    firstTimeUpdate(worksheet, current_followers_dictionary)
    newFollowers = updateFollowers(worksheet, current_followers_dictionary)
    print("Updating your google spreadsheet ...")
    insertNewFollowers(newFollowers, worksheet)
    print("\nUpdate completed.")

# user id for flyingfrugalwithrosie
emma = "37836191304"
run(emma)
