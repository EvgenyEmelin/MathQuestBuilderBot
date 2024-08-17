import json
import xml.etree.ElementTree as ET
import requests

url = 'http://147.45.158.61:9999/get_tasks'
data = [
    {
        'uuid': "0c2f20c6-9191-41da-14e7-5e858bbb7fd7",
            'count': 1,
            'topic': "Определитель с переменной x"
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