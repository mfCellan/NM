import requests
import json
import datetime
import os

def dataformat(format):
    set_time = datetime.datetime.now()
    month = str(set_time.month)
    day = str(set_time.day)
    if set_time.month < 10:
        month = '0' + month

    if set_time.day < 10:
        month = '0' + day

    if format == 'rec':
        return str(set_time.day) + '.' + month + '.' + str(set_time.year) + ' ' + str(set_time.hour) + ':' + str(set_time.minute)
    elif format == 'fn':
        return '_'+str(set_time.year) + '-' + month + '-' + str(set_time.day) + 'T' + str(set_time.hour) + '-' + str(set_time.minute)

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
    new_file_address = path+'/'+user['username']+dataformat('fn')+'.txt'
    if os.path.exists(file_address):
        os.renames(file_address, new_file_address)
    file = open(file_address, 'w')
    file.write(user['name']+' <'+user['email']+ '> '+dataformat('rec')+'\n')
    file.write(user['company']['name']+'\n\n')
    file.write('Завершенные задачи: \n')
    file.write(finished_list+'\n')
    file.write('Оставшиеся задачи: \n')
    file.write(unfinished_list + '\n')
    file.close()


