# Script in python3 to gather user data on github based on search string
#
# Input:
# Search string (change double quotes to %22 and blank spaces to +)
# Github token (https://techmonger.github.io/58/github-token-authentication/)
# Specific number page (optional)
#
# Output:
# Will generate a csv file with the same name as the Search string
#
# Example:
# python ./githubcrawler.py test+engineer 45321dfd6537493747482a42f54be5f
# will get data from page 1 to the end based on the search string and generate test+engineer.csv
# python ./githubcrawler.py test+engineer 45321dfd6537493747482a42f54be5f 5
# will get data from page 5 to the end based on the search string and generate test+engineer.csv
#
# Notes:
# The API only gets the 1000 first results of any Search string
# The Sleep is needed because GitHub API only accepts 30 calls in a minute

import sys
import json
import urllib.request
import time

search = sys.argv[1]
result = open(search + ".csv","a+")
token = sys.argv[2]
header = {'Authorization': 'token ' + token }

apiCalls = 1
page = 1
if(len(sys.argv) == 4):
    page = int(sys.argv[3])

contents = json.loads(urllib.request.urlopen("https://api.github.com/search/users?q=" + search + "&page=" + str(page)).read())
totalUsers = contents["total_count"]
if(totalUsers > 1000):
    totalUsers = 1000
if(len(sys.argv) == 4):
    totalUsers -= page * 30
currentUsers = len(contents["items"])
print("More " + str(totalUsers) + " to go!")

for user in contents["items"]:
    userContent = json.loads(urllib.request.urlopen(urllib.request.Request(user["url"], headers=header)).read())
    if userContent['email'] is not None:
        id = userContent["name"] if userContent["name"] is not None else userContent["login"]
        data = search + ";" + id + ";" + userContent['email'] + ";" + userContent['html_url'] + ";\n"
        result.write(data)
        print(id + " added!")
    apiCalls = apiCalls + 1
    if apiCalls == 30:
        apiCalls = 0
        print("Resting...")
        time.sleep(60)

totalUsers -= currentUsers
page = page + 1

while(totalUsers > 0):
    contents = json.loads(urllib.request.urlopen("https://api.github.com/search/users?q=" + search + "&page=" + str(page)).read())
    apiCalls = apiCalls + 1
    if apiCalls == 30:
        apiCalls = 0
        print("Resting...")
        time.sleep(60)
    currentUsers = len(contents["items"])
    for user in contents["items"]:
        userContent = json.loads(urllib.request.urlopen(urllib.request.Request(user["url"], headers=header)).read())
        if userContent['email'] is not None:
            id = userContent["name"] if userContent["name"] is not None else userContent["login"]
            data = search + ";" + id + ";" + userContent['email'] + ";" + userContent['html_url'] + ";\n"
            result.write(data)
            print(id + " added!")
        apiCalls = apiCalls + 1
        if apiCalls == 30:
            apiCalls = 0
            print("Resting...")
            time.sleep(60)
    totalUsers -= currentUsers
    page = page + 1
    print("More " + str(totalUsers) if totalUsers > 0 else "0" + " to go!")
    print("Page: " + str(page))
print("Finished :)")
result.close()