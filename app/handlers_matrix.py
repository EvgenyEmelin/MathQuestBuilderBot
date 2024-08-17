from aiogram import F, Router, types
from app.keyboard import reply_keyboard_topic, reply_keyboard_subtopic_matrix, reply_keyboard_subtopic_determinant
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
import json
import logging
import asyncio



router = Router()

#Обработка матрицы
def format_matrix(matrix):
    return '\n'.join(['\t'.join(map(str, row)) for row in matrix])


# Обработчик команды /start
@router.message(Command('start'))
async def start(message: Message):
    await message.reply("Привет! Я бот, который генерирует задачки. Выбери из меню ниже, что ты хочешь сделать?", reply_markup=reply_keyboard_topic)


# Обработчик кнопки 'Назад'
@router.message(F.text == 'Назад')
async def start(message: Message):
    await message.reply("Окей, давай вернемся назад", reply_markup=reply_keyboard_topic)

# Обработчик команды кнопки 'Матрицы и операции над ними'
@router.message(F.text == 'Матрицы и операции над ними')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Матрицы и операции над ними"', reply_markup=reply_keyboard_subtopic_matrix)

# Обработчик команды кнопки 'Определители'
@router.message(F.text == 'Определители')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Определители"', reply_markup=reply_keyboard_subtopic_determinant)

# Определение состояний

class FormStates(StatesGroup):
    waiting_for_answer = State()

def escape_markdown(text: str) -> str:
    # Экранирование специальных символов MarkdownV2
    special_characters = ['*', '_', '[', ']', '(', ')', '~', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_characters:
        text = text.replace(char, f'\\{char}')  # Экранируем каждый специальный символ
    return text

def format_matrix(matrix):
    return '\n'.join(['\t'.join(map(str, row)) for row in matrix])


@router.message(F.text == 'Сумма матриц')
async def get_tasks(message: Message, state: FSMContext):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "c4703c4b-e322-4b5c-7c6c-d1652ce84bd8",
            'count': 1,
            'topic': "Сумма матриц"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            first_matrix = task['data']['first']
            second_matrix = task['data']['second']
            answer = task['answer']

            # Формирование сообщения с использованием Markdown
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Первая матрица:*\n{format_matrix(first_matrix)}\n\n"
                f"*Вторая матрица:*\n{format_matrix(second_matrix)}\n\n"
                f"*Введите ваш ответ (через пробелы):*"
            )

            await message.reply(message_text, parse_mode="Markdown")

            # Сохраняем правильный ответ в состоянии
            await state.update_data(correct_answer=answer)
            await state.set_state(FormStates.waiting_for_answer)

            return  # Завершение функции, чтобы ждать следующего сообщения
    else:
        await message.reply('Ошибка при получении задач.')


@router.message(FormStates.waiting_for_answer)
async def check_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    correct_answer = user_data.get('correct_answer')

    # Получаем ответ пользователя и разбиваем его на строки
    user_answer_lines = message.text.strip().split('\n')

    # Преобразуем ввод пользователя в матрицу
    user_answer = []
    try:
        for line in user_answer_lines:
            row = list(map(int, line.split()))
            user_answer.append(row)

        # Проверка ответа пользователя
        if user_answer == correct_answer:
            await message.reply("Верно!")
        else:
            await message.reply(f"Неверно. Правильный ответ:\n{format_matrix(correct_answer)}")

    except ValueError:
        await message.reply("Ошибка: Пожалуйста, убедитесь, что вы вводите только числа, разделенные пробелами.")

    # Сброс состояния после проверки
    await state.set_state(None)  # Завершение состояния


# Хэндлер запроса на тему "Произведение матрицы 3х3 на число"
@router.message(F.text == 'Произведение матрицы 3х3 на число')
async def get_tasks(message: Message, state: FSMContext):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "028c1f3c-e728-46a1-3d3f-d037aa1c813d",
            'count': 1,
            'topic': "Произведение матрицы 3х3 на число"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrix = task['data']['matrix']
            number = task['data']['number']
            correct_answer = task['answer']

            # Формирование сообщения с использованием Markdown
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Матрица:* \n{format_matrix(matrix)}\n\n"
                f"*Число:* {number}\n\n"
                f"*Введите ваш ответ (через пробелы):*"
            )

            await message.reply(message_text, parse_mode='Markdown')

            # Сохраняем правильный ответ в состоянии
            await state.update_data(correct_answer=correct_answer)
            await state.set_state(FormStates.waiting_for_answer)

            return  # Завершение функции, чтобы ждать следующего сообщения
    else:
        await message.reply('Ошибка при получении задач.')


@router.message(FormStates.waiting_for_answer)
async def check_answer(message: Message, state: FSMContext):
    user_data = await state.get_data()
    correct_answer = user_data.get('correct_answer')

    # Получаем ответ пользователя и разбиваем его на строки
    user_answer_lines = message.text.strip().split('\n')

    # Преобразуем ввод пользователя в матрицу
    user_answer = []
    try:
        for line in user_answer_lines:
            row = list(map(int, line.split()))
            user_answer.append(row)

        # Проверка ответа пользователя
        if user_answer == correct_answer:
            await message.reply("Верно!")
        else:
            await message.reply(f"Неверно. Правильный ответ:\n{format_matrix(correct_answer)}")

    except ValueError:
        await message.reply("Ошибка: Пожалуйста, убедитесь, что вы вводите только числа, разделенные пробелами.")

    # Сброс состояния после проверки
    await state.set_state(None)  # Завершение состояния

# Хэндлер запроса на тему "Размер матрицы"
@router.message(F.text == 'Размер матрицы')
async def get_tasks(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "77d65971-cc85-4455-0723-1f21a82b88f1",
            'count': 1,
            'topic': "Размер матрицы"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrix = task['data']
            correct_answer = task['answer']

            # Экранирование символов для MarkdownV2
            correct_answer_text = f"{correct_answer[0]} строк и {correct_answer[1]} столбца."
            correct_answer_text = correct_answer_text.replace('.', '\\.')  # Экранирование точки

            # Формирование сообщения с использованием MarkdownV2
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Матрица:* \n{format_matrix(matrix)}\n\n"
                f"*Правильный ответ:* \n||{correct_answer_text}||"  # Заблюренный текст
            )

            await message.reply(message_text, parse_mode='MarkdownV2')
    else:
        await message.reply('Ошибка при получении задач.')

# Хэндлер запроса на тему "Элемент матрицы"
@router.message(F.text == 'Элемент матрицы')
async def get_tasks(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "b22fae57-4b10-4d50-740a-06956656bef1",
            'count': 1,
            'topic': "Элемент матрицы"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrix = task['data']['matrix']
            row_index = task['data']['row_index']
            column_index = task['data']['column_index']
            correct_answer = task['answer']

            # Экранируем текст для MarkdownV2
            question = escape_markdown(question)
            matrix_text = escape_markdown(format_matrix(matrix))
            correct_answer = escape_markdown(str(correct_answer))

            # Изменяем формат индекса
            index_text = f"A {row_index + 1}, {column_index + 1}"  # Изменено, чтобы избежать использования ( и )

            # Формирование сообщения с использованием MarkdownV2
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Матрица:* \n{matrix_text}\n\n"
                f"*Индекс элемента:* {index_text}\n\n"  # Изменено
                f"*Правильный ответ:* ||{correct_answer}||"
            )

            await message.reply(message_text, parse_mode='MarkdownV2')
    else:
        await message.reply('Ошибка при получении задач.')

# Хэндлер запроса на тему "Транспонирование"
@router.message(F.text == 'Транспонирование')
async def get_tasks(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "0c2f20c6-9191-41da-14e7-5e858bbb7fd7",
            'count': 1,
            'topic': "Транспонирование"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrix = task['data']
            correct_answer = task['answer']

            # Формирование сообщения с использованием MarkdownV2
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Исходная матрица:* \n{format_matrix(matrix)}\n\n"
                f"*Транспонированная матрица:* \n||{format_matrix(correct_answer)}||"  # Заблюренный текст
            )

            await message.reply(message_text, parse_mode='MarkdownV2')
    else:
        await message.reply('Ошибка при получении задач.')

# Хэндлер запроса на тему "Произведение двух матриц (3х3)"
@router.message(F.text == 'Произведение двух матриц (3х3)')
async def get_tasks(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "4f6241db-b8b2-4cf0-182b-9d468f0a2d83",
            'count': 1,
            'topic': "Произведение двух матриц (3х3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrices = task['data']
            correct_answer = task['answer']

            # Экранируем текст для MarkdownV2
            question = escape_markdown(question)
            matrix1 = escape_markdown(format_matrix(matrices['matrix1']))
            matrix2 = escape_markdown(format_matrix(matrices['matrix2']))
            result = escape_markdown(format_matrix(correct_answer))

            # Формирование сообщения с использованием MarkdownV2
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Матрица 1:* \n{matrix1}\n\n"
                f"*Матрица 2:* \n{matrix2}\n\n"
                f"*Результат умножения матриц:* \n||{result}||"  # Используем обратные кавычки
            )

            await message.reply(message_text, parse_mode='MarkdownV2')
    else:
        await message.reply('Ошибка при получении задач.')

#############################___ОПРЕДЕЛИТЕЛИ___####################################
#Хэндлер запроса на тему "Вычислить определитель (3х3)"
@router.message(F.text == 'Вычислить определитель (3х3)')
async def get_tasks(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "0c2f20c6-9191-41da-14e7-5e858bbb7fd7",
            'count': 1,
            'topic': "Определитель с переменной x"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrix = task['data']
            answer = task['answer']

            # Проверка типа данных и округление
            if isinstance(answer, (int, float)):
                determinant = round(answer)  # Округление до целого числа
            else:
                determinant = "Ошибка: Неверный тип данных для определителя"

            # Формирование сообщения с использованием Markdown
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Матрица A:* \n{format_matrix(matrix)}\n\n"
                f"*Определитель матрицы A:* ||{determinant}||"
            )

            await message.reply(message_text, parse_mode='MarkdownV2')
    else:
        await message.reply('Ошибка при получении задач.')

#Хэндлер запроса на тему "Уравнение в определителе (3х3)"
@router.message(F.text == 'Уравнение в определителе (3х3)')
async def get_tasks(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "3b5b6b10-c9a5-4358-0079-3e9459f53f9f",
            'count': 1,
            'topic': "Уравнение в определителе (3х3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = task['task']
            matrix = task['data']['matrix']
            target_determinant = task['data']['determinant']
            value_of_x = task['answer']

            # Формирование сообщения с использованием Markdown
            message_text = (
                f"*Вопрос:* {question}\n\n"
                f"*Матрица:* \n{format_matrix(matrix)}\n\n"
                f"*Целевой определитель:* {target_determinant}\n\n"
                f"*Значение, которое должно стоять на месте x:* {value_of_x}"
            )

            await message.reply(message_text, parse_mode='Markdown')
    else:
        await message.reply('Ошибка при получении задач.')







