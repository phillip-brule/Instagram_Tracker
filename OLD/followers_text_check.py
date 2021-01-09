import json

def readFollowers():
    f = open("D:\\Phill\\Documents\\Instagram_App\\followers.txt", "r")
    followers_string = f.read()
    f.close()    
    followers_dictionary = json.loads(followers_string)
    return followers_dictionary

followers = readFollowers()
sorted_follower_id = sorted(followers['ids'])

has_duplicates = False
previous_id = -1
for id in sorted_follower_id:
    if id == previous_id:
        print("Duplicate Found: ")
        print(id)
        has_duplicates = True
    previous_id = id

if has_duplicates == False:
    print("No duplicates")

i=0
for user in followers["ids"]:
    i += 1
print(i)
