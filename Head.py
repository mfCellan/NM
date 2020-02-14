import requests
import json
import datetime
import os


def format_date():  # Функция для получения времени в формате ДД.ММ.ГГГГ ЧЧ:ММ:CC
    set_time = datetime.datetime.now()
    m = str(set_time.month)
    d = str(set_time.day)
    h = str(set_time.hour)
    min = str(set_time.minute)
    sec = str(set_time.second)
    if set_time.second < 10:
        sec = '0' + sec
    if set_time.month < 10:
        m = '0' + m
    if set_time.day < 10:
        d = '0' + d
    if set_time.hour < 10:
        h = '0' + h
    if set_time.minute < 10:
        min = '0' + min
    return d + '.' + m + '.' + str(set_time.year) + ' ' + h + ':' + min + ':' + sec


path = os.getcwd()  # получаем директорию в которой хранится скрипт
path += "/tasks"
if not (os.path.exists(path)):  # если отсутствует директория tasks то создаём её
    os.mkdir(path)
req_users = requests.get("https://json.medrating.org/users")  # Делаем запрос в API с пользователями
req_tasks = requests.get("https://json.medrating.org/todos")  # Делаем запрос в API с задачами
users = json.loads(req_users.text)  # Десериализируем JSON файл с пользователями
tasks = json.loads(req_tasks.text)  # Десериализируем JSON файл с заданиями
for user in users:
    finished_list = ''  # Строка для хранения выполненных заданий
    unfinished_list = ''  # Строка для хранения не выполненных заданий
    for task in tasks:  # Поиск для каждого пользователя выполненных и не выполненных заданий
        if task['userId'] == user['id']:  # Проверка на принадлежность задачи конкретному пользователю
            if task['completed']:  # Проверка статуса готовности задани (выполнена, не выполнена)
                if len(task['title']) > 50:  # Если кол-во символов в названии > 50 то обрезать  до 50ти символов
                    finished_list += task['title'][0:50] + '...\n'
                else:
                    finished_list += task['title'] + '\n'  # Добавить задачу в список решённых задач
            else:
                if len(task['title']) > 50:  # Если кол-во символов в названии > 50 то обрезать  до 50ти символов
                    unfinished_list += task['title'][0:50] + '...\n'
                else:
                    unfinished_list += task['title'] + '\n'  # Добавить задачу в список решённых задач
    file_address = path + '/' + user['username'] + '.txt'  # Имя файла для пользователя
    if os.path.exists(file_address):  # Проверка на существование файла с таким именем
        file = open(file_address, 'r')
        date = file.readline()  # Считываем первую строку фала чтобы получить время создания отчета
        file.close()
        t = date[len(date) - 9:len(date) - 1]  # получение времени создание файла
        t = t.replace(':', '-')  # замена : на - , т.к. в название файла нельзя использовать :
        y = date[len(date) - 14:len(date) - 10]  # получение года создание файла
        m = date[len(date) - 17:len(date) - 15]  # получение месяца создание файла
        d = date[len(date) - 20:len(date) - 18]  # получение дня создание файла
        new_file_address = path + '/' + user['username'] + '_' + y + '-' + m + '-' + d + 'T' + t + '.txt'
        os.renames(file_address, new_file_address)  # Переименование старого отчета
    file = open(file_address, 'w')  # Открытие файла для записи
    file.write(user['name'] + ' <' + user['email'] + '> ' + format_date() + '\n')  # Записываем имя, email, дату и время
    file.write(user['company']['name'] + '\n\n')  # Записываем название компании в которой работает пользователь
    if not(len(finished_list) == 0):
        file.write('Завершенные задачи: \n')
        file.write(finished_list + '\n')  # Записываем завершенные задачи пользователя
    else:  # Если нет завершенных задач то сообщаем об этом
        file.write('Завершенных задач нет \n')
    if not(len(unfinished_list) == 0):
        file.write('Оставшиеся задачи: \n')
        file.write(unfinished_list + '\n')  # Записываем не завершенные задачи пользователя
    else:  # Если нет не завершенных задач то сообщаем об этом
        file.write('Оставшихся задач нет \n')
    file.close()
