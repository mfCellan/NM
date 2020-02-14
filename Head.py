import requests
import json
import datetime
import os

def dataformat(format):
    set_time = datetime.datetime.now()
    month = str(set_time.month)
    day = str(set_time.day)
    hour = str(set_time.hour)
    minute = str(set_time.minute)
    if set_time.month < 10:
        month = '0' + month

    if set_time.day < 10:
        day = '0' + day

    if set_time.hour < 10:
        hour = '0' + hour

    if set_time.minute < 10:
        minute = '0' + minute

    if format == 'rec':
        return day + '.' + month + '.' + str(set_time.year) + ' ' + hour + ':' + minute
    elif format == 'fn':
        return '_'+str(set_time.year) + '-' + month + '-' + str(set_time.day) + 'T' + hour + '-' + minute

path = os.getcwd()
path += "/tasks"
if not(os.path.exists(path)):
    os.mkdir(path)


req_users = requests.get("https://json.medrating.org/users")
req_tasks = requests.get("https://json.medrating.org/todos")
users = json.loads(req_users.text)
tasks = json.loads(req_tasks.text)


for user in users:
    finished_list = ''
    unfinished_list = ''
    for task in tasks:

        if task['userId'] == user['id']:
            if task['completed']:
                if len(task['title']) > 50:
                    finished_list += task['title'][0:50] + '...\n'
                else:
                    finished_list += task['title'] + '\n'
            else:
                if len(task['title']) > 50:
                    unfinished_list += task['title'][0:50] + '...\n'
                else:
                    unfinished_list += task['title']+'\n'
    file_address = path+'/'+user['username']+'.txt'
    if os.path.exists(file_address):
        file = open(file_address, 'r')
        date = file.readline()
        file.close()
        time = date[len(date)-6:len(date)-1]
        time = time.replace(':', '-')
        year = date[len(date)-11:len(date)-7]
        month = date[len(date)-14:len(date)-12]
        day = date[len(date)-17:len(date)-15]

        new_file_address = path + '/' + user['username'] + '_' + year + '-' + month + '-'+day+'T'+time+'.txt'
        os.renames(file_address, new_file_address)
    file = open(file_address, 'w')
    file.write(user['name']+' <'+user['email']+ '> '+dataformat('rec')+'\n')
    file.write(user['company']['name']+'\n\n')
    file.write('Завершенные задачи: \n')
    file.write(finished_list+'\n')
    file.write('Оставшиеся задачи: \n')
    file.write(unfinished_list + '\n')
    file.close()
# file = open('C:/Users/rock1/Desktop/Work/tasks/Bret.txt', 'r')
# str = file.readline()
# print('time:', str[len(str)-6:len(str)])  # time
# print('year:', str[len(str)-11:len(str)-7])  # year
# print('month:', str[len(str)-14:len(str)-12])  # month
# print('day:', str[len(str)-17:len(str)-15])  # day


