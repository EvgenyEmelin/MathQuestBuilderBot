from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton
import json

reply_keyboard_topic = ReplyKeyboardMarkup(keyboard=[
            [
                KeyboardButton(text='Матрицы и операции над ними'),
            ],
            [
                KeyboardButton(text='Определители'),
            ],
        ],
        resize_keyboard=True,
        one_time_keyboard=False
    )
reply_keyboard_subtopic_matrix = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Сумма матриц'),
        KeyboardButton(text='Произведение матрицы 3х3 на число'),
    ],

    [
        KeyboardButton(text='Размер матрицы'),
        KeyboardButton(text='Элемент матрицы'),
    ],
    [
        KeyboardButton(text='Транспонирование'),
        KeyboardButton(text='Произведение двух матриц (3х3)'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_determinant = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Вычислить определитель (3х3)'),
        KeyboardButton(text='Уравнение в определителе (3х3)'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)


