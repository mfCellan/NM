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
    exist_finished_task = False
    exist_unfinished_task = False
    for task in tasks:

        if task['userId'] == user['id']:

            if task['completed']:
                exist_finished_task = True
                if len(task['title']) > 50:
                    finished_list += task['title'][0:50] + '...\n'
                else:
                    finished_list += task['title'] + '\n'
            else:
                exist_unfinished_task = True
                if len(task['title']) > 50:
                    unfinished_list += task['title'][0:50] + '...\n'
                else:
                    unfinished_list += task['title']+'\n'
    file_address = path+'/'+user['username']+'.txt'
    if os.path.exists(file_address):
        file = open(file_address, 'r')
        date = file.readline()
        file.close()
        hour = date[len(date)-6:len(date)-4]
        minute = date[len(date)-3:len(date)-1]
        year = date[len(date)-11:len(date)-7]
        month = date[len(date)-14:len(date)-12]
        day = date[len(date)-17:len(date)-15]
        d = datetime.datetime(int(year), int(month), int(day), int(hour), int(minute))
        if (d - datetime.datetime.now()).seconds >= 60:
            new_file_address = path + '/' + user['username'] + '_' + year + '-' + month + '-'+day+'T'+hour+'-' + minute + '.txt'
            os.renames(file_address, new_file_address)
            file = open(file_address, 'w')
            file.write(user['name'] + ' <' + user['email'] + '> ' + dataformat('rec') + '\n')
            file.write(user['company']['name'] + '\n\n')
            if exist_finished_task or exist_unfinished_task:
                if exist_finished_task:
                    file.write('Завершенные задачи: \n')
                    file.write(finished_list + '\n')
                else:
                    file.write('Завершенных задач нет \n')

                if exist_unfinished_task:
                    file.write('Оставшиеся задачи: \n')
                    file.write(unfinished_list + '\n')
                else:
                    file.write('Оставшихся задач нет \n')
            else:
                file.write('У пользователя нет задач \n')
            file.close()
        else: print('нельзя создавать новый фал чаще чем через 1 минуту')


