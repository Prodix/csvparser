import csv
import json
import names
import time
import asyncio

# write all users to csv
def writeUsers(usersList):
    with open('file.csv', 'a') as csvfile:
        fieldnames = ['id', 'first_name', 'last_name']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for i in usersList:
            writer.writerows(i)

# read users from csv and dump to json
def readUsers():
    usersDict = {}
    with open('file.csv') as csvfile:
        reader = csv.DictReader(csvfile)
        with open('file.json', 'w') as jsonfile:
            for row in reader:
                usersDict[row['id']] = row['first_name'] + ' ' + row['last_name']

            json.dump(usersDict, jsonfile, indent=4)

# user generate
async def usersGenerator(userCount, usersList, index):
    for i in range(userCount*index+1, userCount+1+userCount*index):
        usersList[index].append({'id': i, 'first_name': names.get_first_name(), 'last_name': names.get_last_name()})

# task generator
async def main(usersList, taskCount, allUsers):
    taskSet = set()
    for i in range(taskCount):
        task = asyncio.create_task(usersGenerator(int(allUsers/taskCount), usersList, i))
        taskSet.add(task)
    asyncio.gather(*taskSet)

if __name__ == "__main__":
    taskCount = 10000
    allUsers = 100000
    usersList = [[] for i in range(taskCount)]

    with open('file.csv', 'w') as file:
        pass

    time1 = time.time() # time before start
    asyncio.run(main(usersList, taskCount, allUsers))
    print(time.time()-time1, " seconds") # timediff

    writeUsers(usersList) # write to csv
    readUsers() # dump to json