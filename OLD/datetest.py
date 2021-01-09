from datetime import datetime
import time
import json

def load_clients():
    f = open("D:\\Phill\\Documents\\Instagram_App\\clients.txt", "r", encoding="utf8")
    client_string = f.read()
    f.close()    
    return json.loads(client_string)

client_dictionary = load_clients()
days = client_dictionary["days_to_wait"][0]


date = "4/11/2020"
cdate = datetime.now()
py_date = datetime.strptime(date, "%d/%m/%Y")
difference = abs((cdate - py_date).days)
if difference >= days:
    print(True)
else:
    print(False)