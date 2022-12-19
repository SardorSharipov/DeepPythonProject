from telebot import types

force = types.ForceReply()

help_markup = types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(text="Ввод данных 👩‍💻", callback_data='0'),
            types.InlineKeyboardButton(text="Почему ошибка? 😡", callback_data='1')
        ],
        [
            types.InlineKeyboardButton(text="Зачем мне Бот? 🤡", callback_data='2'),
            types.InlineKeyboardButton(text="Как работает Бот 🤔", callback_data='3')
        ],
        [
            types.InlineKeyboardButton(text="Главное меню 🔠", callback_data='menu')
        ]
    ]
)

menu_markup = types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(text='Команды 🏦', callback_data='commands'),
            types.InlineKeyboardButton(text='Цель 🏆', callback_data='goal'),
            types.InlineKeyboardButton(text='Помощь 🤝', callback_data='help')
        ],
        [
            types.InlineKeyboardButton(text='Ввод покупок ⤵', callback_data='input'),
            types.InlineKeyboardButton(text='Вывод покупок ⤴', callback_data='output')
        ]
    ]
)

command_markup = types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(text='Главное меню 🔠', callback_data='menu')
        ]
    ]
)

analysis_markup = types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(text='График расходов 📈', callback_data='graphic'),
        ],
        [
            types.InlineKeyboardButton(text='Круговая Диаграмма Категорий 🧿', callback_data='pie'),
        ],
        [
            # types.InlineKeyboardButton(text='Удалить покупки ❌', callback_data='delete_purchase'),
            types.InlineKeyboardButton(text='Фильтр ✂', callback_data='filter_purchase')
        ],
        [
            types.InlineKeyboardButton(text='Главное меню 🔠', callback_data='menu'),
        ]
    ]
)

filter_markup = types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(text='За Сегодня 📝', callback_data='today'),
        ],
        [
            types.InlineKeyboardButton(text='За этот месяц 📑', callback_data='month'),
        ],
        [
            types.InlineKeyboardButton(text='За всё время 🛒', callback_data='all_time'),
        ],
        [
            types.InlineKeyboardButton(text='Главное меню 🔠', callback_data='menu'),
        ]
    ]
)

goal_markup = types.InlineKeyboardMarkup(
    [
        [
            types.InlineKeyboardButton(text='Добавить в Сбережения ❎', callback_data='add_goal'),
        ],
        [
            types.InlineKeyboardButton(text='Удалить Цель ❌', callback_data='delete_goal'),
        ],
        [
            types.InlineKeyboardButton(text='Главное меню 🔠', callback_data='menu'),
        ]
    ]
)
