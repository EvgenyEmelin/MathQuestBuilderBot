from aiogram import F, Router, types
from app.keyboard import (reply_keyboard_topic, reply_keyboard_subtopic_matrix, reply_keyboard_subtopic_matrix_equations,reply_keyboard_subtopic_determinant,reply_keyboard_subtopic_reverse_matrix,
                          reply_keyboard_subtopic_systems_of_linear_equations, reply_keyboard_subtopic_rank_of_matrix,reply_keyboard_subtopic_vectors, reply_keyboard_subtopic_straight_line_on_a_plane, reply_keyboard_subtopic_straight_line_in_space)
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
import requests
import json
import re


router = Router()

#Обработка матрицы
def format_matrix(matrix):
    return '\n'.join(['\t'.join(map(str, row)) for row in matrix])

# Функция для создания безопасной строки
def create_safe_string(text):
    special_chars = ['-', '_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '=', '|', '{', '}', '.', '!']
    safe_text = text
    for char in special_chars:
        safe_text = safe_text.replace(char, '')
    return safe_text

# Функция для экранирования специальных символов в MarkdownV2
def escape_markdown(text):
    """Экранирование специальных символов для MarkdownV2"""
    # Экранируем специальные символы
    special_chars = ['_', '*', '[', ']', '(', ')', '~', '`', '>', '#', '+', '-', '=', '|', '{', '}', '.', '!']
    for char in special_chars:
        text = text.replace(char, f'\\{char}')  # Экранируем каждый специальный символ
    return text


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


# Обработчик команды кнопки 'Обратная матрица'
@router.message(F.text == 'Обратная матрица')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Обратная матрица"', reply_markup=reply_keyboard_subtopic_reverse_matrix)

# Обработчик команды кнопки 'Матричные уравнения'
@router.message(F.text == 'Матричные уравнения')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Матричные уравнения"', reply_markup=reply_keyboard_subtopic_matrix_equations)

# Обработчик команды кнопки 'Системы линейных уравнений'
@router.message(F.text == 'Системы линейных уравнений')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Системы линейных уравнений"', reply_markup=reply_keyboard_subtopic_systems_of_linear_equations)

# Обработчик команды кнопки 'Ранг матрицы'
@router.message(F.text == 'Ранг матрицы')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Ранг матрицы"', reply_markup=reply_keyboard_subtopic_rank_of_matrix)

# Обработчик команды кнопки 'Векторы'
@router.message(F.text == 'Векторы')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Векторы"', reply_markup=reply_keyboard_subtopic_vectors)

# Обработчик команды кнопки 'Прямая на плоскости'
@router.message(F.text == 'Прямая на плоскости')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Прямая на плоскости"', reply_markup=reply_keyboard_subtopic_straight_line_on_a_plane)

# Обработчик команды кнопки 'Плоскость в пространстве'
@router.message(F.text == 'Плоскость в пространстве')
async def topic_matrix(message: Message):
    await message.reply('Давай подберем тебе задачи по теме "Плоскость в пространстве"', reply_markup=reply_keyboard_subtopic_straight_line_in_space)

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


#-------------------------------------------------------------------ОПРЕДЕЛИТЕЛЬ----------------------------------------------------------

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

#---------------------------------------------------------------ОБРАТНАЯ МАТРИЦА-------------------------------------------

# Хэндлер запроса на тему "Обратная матрица (3х3)"
@router.message(F.text == 'Обратная матрица (3х3)')
async def get_inverse_matrix(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "f1579922-863b-424f-2044-edd7c3bd437a",
            'count': 1,
            'topic': "Обратная матрица (3х3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()
        for task in tasks:
            question = create_safe_string(task['task'])  # Создаем безопасную строку для вопроса
            matrix = task['data']
            answer = task['answer']

            # Округление элементов обратной матрицы до 3 знаков после запятой
            rounded_answer = [[round(element, 3) for element in row] for row in answer]

            # Формирование сообщения с использованием HTML
            message_text = (
                f"<b>Вопрос:</b> {question}\n"
                f"<b>Матрица A:</b>\n{format_matrix(matrix)}\n"
                f"<b>Обратная матрица A^-1:</b>\n||{format_matrix(rounded_answer)}||"  # Заблюривание обратной матрицы
            )

            await message.reply(message_text, parse_mode='HTML')
    else:
        await message.reply('Ошибка при получении задач.')

# Хэндлер запроса на тему "Элемент обратной матрицы (3х3)"
@router.message(F.text == 'Элемент обратной матрицы(3х3)')
async def get_inverse_matrix_element(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "b07318ac-c462-4d51-9f25-052c36eb4d3f",
            'count': 1,
            'topic': "Элемент обратной матрицы(3х3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()  # Получаем список задач
        for task in tasks:
            question = create_safe_string(task['task'])  # Создаем безопасную строку для вопроса
            matrix_data = task['data']  # Извлекаем данные матрицы
            answer = task['answer']  # Извлекаем ответ

            # Получение данных матрицы и индексов
            matrix = matrix_data['matrix']  # Извлекаем матрицу
            row_index = matrix_data['rowIndex']  # Индекс строки
            col_index = matrix_data['columnIndex']  # Индекс столбца

            # Получение элемента матрицы
            element = round(answer, 3)  # Округляем ответ до 3 знаков после запятой
            blurred_element = f"||{element}||"  # Заблюривание элемента

            # Формирование сообщения
            message_text = (
                f"Вопрос: {question}\n"
                f"Матрица A: \n{format_matrix(matrix)}\n"
                f"Элемент (строка {row_index + 1}, столбец {col_index + 1}) обратной матрицы A^-1: {blurred_element}"
            )

            await message.reply(message_text)
    else:
        await message.reply('Ошибка при получении задач.')

#------------------------------------------------Матричные уравнения----------------------------------------------
# Хэндлер запроса на тему "Матричное уравнение (AX=B,3x3)"
@router.message(F.text == 'Матричное уравнение (AX=B,3x3)')
async def solve_equation(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "7ae48f49-aecf-4006-c95d-af63a3260eb0",
            'count': 1,
            'topic': "Матричное уравнение (AX=B,3x3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()  # Получаем список задач
        for task in tasks:
            question = task['task']  # Используем вопрос без экранирования
            matrix_A = task['data']['A']  # Извлекаем матрицу A
            matrix_B = task['data']['B']  # Извлекаем матрицу B
            answer = task['answer']  # Извлекаем ответ

            # Округление элементов ответа до 3 знаков после запятой
            rounded_answer = [[round(element, 3) for element in row] for row in answer]

            # Формирование сообщения с использованием HTML
            message_text = (
                f"<b>Вопрос:</b> {question}\n"
                f"<b>Матрица A:</b>\n{format_matrix(matrix_A)}\n"
                f"<b>Матрица B:</b>\n{format_matrix(matrix_B)}\n"
                f"<b>Ответ X:</b>\n{format_matrix(rounded_answer)}"  # Вывод ответа
            )

            await message.reply(message_text, parse_mode='HTML')
    else:
        await message.reply('Ошибка при получении задач.')

# Хэндлер запроса на тему "Решите уравнение вида AXB = C"
@router.message(F.text == 'Матричное уравнение (AXB=C,3x3)')
async def solve_equation(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "6463aa54-da58-4751-8578-72ab9670ec74",  # Замените на ваш UUID
            'count': 1,
            'topic': "Матричное уравнение (AXB=C,3x3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()  # Получаем список задач
        for task in tasks:
            question = task['task']  # Извлекаем вопрос
            matrix_A = task['data']['A']  # Извлекаем матрицу A
            matrix_B = task['data']['B']  # Извлекаем матрицу B
            matrix_C = task['data']['C']  # Извлекаем матрицу C
            answer = task['answer']  # Извлекаем ответ

            # Округление элементов ответа до 3 знаков после запятой
            rounded_answer = [[round(element, 3) for element in row] for row in answer]

            # Формирование сообщения
            message_text = (
                f"Вопрос: {question}\n"
                f"Матрица A:\n{format_matrix(matrix_A)}\n"
                f"Матрица B:\n{format_matrix(matrix_B)}\n"
                f"Матрица C:\n{format_matrix(matrix_C)}\n"
                f"Ответ X:\n{format_matrix(rounded_answer)}"  # Вывод ответа
            )

            await message.reply(message_text)  # Отправка сообщения без MarkdownV2
    else:
        await message.reply('Ошибка при получении задач.')

#------------------------------------------------СЛУ----------------------------------------------

# Хэндлер запроса на тему "Решите систему линейных уравнений"
@router.message(F.text == 'СЛУ (3x3)')
async def solve_system(message: Message):
    url = 'http://147.45.158.61:9999/get_tasks'
    data = [
        {
            'uuid': "d53761d3-4270-4af4-5f21-b7caaa4efb43",
            'count': 1,
            'topic': "СЛУ (3x3)"
        }
    ]

    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        tasks = response.json()  # Получаем список задач
        for task in tasks:
            question = task['task']  # Извлекаем вопрос
            first_equation = task['data']['first_equation']  # Первое уравнение
            second_equation = task['data']['second_equation']  # Второе уравнение
            third_equation = task['data']['third_equation']  # Третье уравнение
            answer = task['answer']  # Извлекаем ответ

            # Округление элементов ответа до 3 знаков после запятой
            rounded_answer = [[round(element, 3) for element in row] for row in answer]

            # Формирование сообщения
            message_text = (
                f"Вопрос: {question}\n"
                f"Первое уравнение: {first_equation}\n"
                f"Второе уравнение: {second_equation}\n"
                f"Третье уравнение: {third_equation}\n"
                f"Ответ: {rounded_answer[0][0]}, {rounded_answer[1][0]}, {rounded_answer[2][0]}"
            )

            await message.reply(message_text)
    else:
        await message.reply('Ошибка при получении задач.')








