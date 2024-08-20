#Данный файл является примером и тестом API запроса, для дальнейшей обработки в handler
#This file is an example and test of an API request for further processing in the handler
import json
import xml.etree.ElementTree as ET
import requests

url = 'http://147.45.158.61:9999/get_tasks'
data = [
    {
        'uuid': "d53761d3-4270-4af4-5f21-b7caaa4efb43",
            'count': 1,
            'topic': "СЛУ 3х3"
    }
]

# Отправка POST-запроса с данными в формате JSON
headers = {'Content-Type': 'application/json'}
response = requests.post(url, headers=headers, data=json.dumps(data))

# Проверка статуса ответа
if response.status_code == 200:
    print('Запрос успешен:', response.json())
else:
    print('Ошибка:', response.status_code, response.text)