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
            [
                KeyboardButton(text='Обратная матрица'),
            ],
            [
                KeyboardButton(text='Матричные уравнения'),
            ],
            [
                KeyboardButton(text='Системы линейных уравнений'),
            ],
            [
                KeyboardButton(text='Ранг матрицы'),
            ],
            [
                KeyboardButton(text='Векторы'),
            ],
            [
                KeyboardButton(text='Прямая на плоскости'),
            ],
            [
                KeyboardButton(text='Плоскость в пространстве'),
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

reply_keyboard_subtopic_reverse_matrix = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Обратная матрица (3х3)'),
        KeyboardButton(text='Элемент обратной матрицы(3х3)'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_matrix_equations = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Матричное уравнение (AX=B,3x3)'),
        KeyboardButton(text='Матричное уравнение (AXB=C,3x3)'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_systems_of_linear_equations = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='СЛУ (3x3)'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_rank_of_matrix = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Ранг матрицы (в пределах (3x3)'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_vectors = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Вычислить скалярное произведение векторов'),
        KeyboardButton(text='Вычислить векторное произведение векторов'),
    ],
    [
        KeyboardButton(text='Вычислить модуль векторного произведения'),
        KeyboardButton(text='Вычислить смешанное произведение векторов'),
    ],
    [
        KeyboardButton(text='Проверка коллинеарности векторов'),
        KeyboardButton(text='Проверка компланарности векторов'),
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_straight_line_on_a_plane = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Составить ур-е прямой через две точки'),
        KeyboardButton(text='Составить ур-е прямой параллельной данной')
    ],
    [
        KeyboardButton(text='Составить ур-е прямой параллельной BC'),
        KeyboardButton(text='Найти точку пересечения прямых AB и CD'),
    ],
    [
        KeyboardButton(text='Определить расстояние от точки до прямой')
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)

reply_keyboard_subtopic_straight_line_in_space = ReplyKeyboardMarkup(keyboard=[
    [
        KeyboardButton(text='Составить ур-е плоскости по 3м точкам (определитель)'),
        KeyboardButton(text='Составить ур-е плоскости по нормали и точке'),
    ],
    [
        KeyboardButton(text='Составить ур-е параллельной плоскости (нормаль и точка)'),
        KeyboardButton(text='Составить ур-е плоскости (2 точки) перпендикулярной данной (точка и нормаль)')
    ],
    [
        KeyboardButton(text='Проекция точки на прямую NM'),
        KeyboardButton(text='Проекция точки на плоскость (точка и нормаль)')
    ],
    [
        KeyboardButton(text='Назад')
    ]
],
    resize_keyboard=True,
    one_time_keyboard=False
)