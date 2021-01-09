import schedule
import json
import time
import insta_google_sheets

def load_clients():
    f = open("D:\\Phill\\Documents\\Instagram_App\\clients.txt", "r")
    client_string = f.read()
    f.close()    
    return json.loads(client_string)

def run():
    client_dictionary = load_clients()
    i = 0
    for user_id in client_dictionary["ids"] :
        #update google spreadsheet
        insta_google_sheets.run(user_id)

        #auto message new users
        username = client_dictionary["usernames"][i]
        password = client_dictionary["passwords"][i]
        message = client_dictionary["messages"][i]
        days = client_dictionary["days_to_wait"][i]
        insta_google_sheets.autoMessageUsers(username, password, message, days)
        i+=1
    return

schedule.every().day.at("01:00").do(run())

while True:
    schedule.run_pending()
    time.sleep(60) # wait one minute