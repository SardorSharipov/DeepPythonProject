import os

import telebot

import markups as markups
import phrases as phrases
from goal import read_goal, check_goal, goal_parser, write_goal
from purchase_info import read_purchase, purchase_to_str, purchase_parsing, write_purchase, delete_purchase, \
    delete_purchases


def add_money_goal_command(e: telebot.types.Message, bot_client: telebot.TeleBot):
    try:
        price = float(e.text)
        if price <= 0.0:
            raise ValueError()
        goal = read_goal(e.chat.id)
        print(e.text)
        goal.price -= price
        print(goal.price)
        answer, message = check_goal(goal)
        if answer:
            show_command(e, bot_client, message, markups.menu_markup)
        else:
            show_command(e, bot_client, message, markups.goal_markup)
    except Exception as ex:
        bot_client.send_message(chat_id=e.chat.id,
                                text="*Некорректные данные о сумме денег 🥴*\n\n" + phrases.ADD_MONEY_REPLY,
                                parse_mode='Markdown',
                                reply_markup=markups.force)
        print(f"[COMMAND] Error {ex}")


def add_goal_command(e: telebot.types.Message, bot_client: telebot.TeleBot):
    try:
        goal = goal_parser(e.text)
        goal.user_id = e.chat.id
        if goal is not None:
            write_goal(goal)
            text = '*Цель Успешно Добавлена ✅*\n\nВыберите дальнейшие действия.'
            show_command(e, bot_client, text, markups.menu_markup)
        else:
            raise ValueError()
    except Exception as ex:
        bot_client.send_message(chat_id=e.chat.id,
                                text="*Некорректные данные о сумме денег 🥴*\n\n" + phrases.NO_GOAL_CHECK,
                                parse_mode='Markdown',
                                reply_markup=markups.force)
        print(f"[COMMAND] Error {ex}")


def get_expense(e: telebot.types.Message, bot_client: telebot.TeleBot):
    try:
        if os.path.exists(f'data/purchases/{e.chat.id}.json'):
            purchases = read_purchase(e.chat.id)
            message = purchase_to_str(purchases)
            show_command(e, bot_client, message, markups.analysis_markup)
        else:
            show_command(e, bot_client, phrases.NO_JSON_MESSAGE, markups.analysis_markup)
    except Exception as ex:
        print(f"[COMMAND] Error {ex}")


def fill_expense(e: telebot.types.Message, bot_client: telebot.TeleBot):
    try:
        temp = 0
        text_lines = e.text.split('\n')
        for i in range(len(text_lines)):
            purchase = purchase_parsing(text_lines[i], e.chat.id)
            if purchase is not None:
                write_purchase(e.chat.id, purchase)
                temp += 1
            else:
                print(f'[Purchase] Wrong Info from {e.chat.id}')
        if temp == 0:
            text = "*Некорректные данные о покупке или покупках 🥴*\n\n" + phrases.REPLY_MESSAGE
            show_command(e, bot_client, text, markups.force)
        else:
            text = f"*Успешно добавлено {temp} из {len(text_lines)} покупок ✅*\n\n" + phrases.REPLY_MESSAGE
            show_command(e, bot_client, text, markups.force)
    except Exception as ex:
        print(f"[COMMAND] Error {ex}")


def add_expense(e: telebot.types.Message, bot_client: telebot.TeleBot):
    try:
        show_command(e, bot_client, phrases.REPLY_MESSAGE, markups.force)
    except Exception as ex:
        print(f"[COMMAND] Error {ex}")


def delete_expense(e: telebot.types.Message, bot_client: telebot.TeleBot):
    try:
        if e.text.isdigit():
            delete_purchase(e.chat.id, int(e.text))
        else:
            borders = e.text.split('-')
            if len(borders) == 2 and borders[0].isdigit() and borders[1].isdigit():
                delete_purchases(e.chat.id, int(borders[0]), int(borders[1]))
            else:
                raise ValueError()
        if len(read_purchase(e.chat.id)) == 0:
            os.remove(f"data/purchases/{e.chat.id}")
            text = "*Ваш список покупок был обновлен 📊*\n\n" \
                   + "*На данный момент Ваш список покупок пуст ☹*"
            show_command(e, bot_client, text, markups.menu_markup)
        else:
            text = "*Ваш список покупок был обновлен 📊*\n\n" + purchase_to_str(read_purchase(e.chat.id))
            show_command(e, bot_client, text, markups.analysis_markup)
    except Exception:
        text = "*Некорректные данные о границах 🥴*\n\n" + phrases.DELETE_PURCHASES_REPLY
        show_command(e, bot_client, text, markups.force)


def show_command(e: telebot.types.Message, bot_client: telebot.TeleBot, text: str, markup):
    try:
        bot_client.send_message(chat_id=e.chat.id,
                                text=text,
                                parse_mode='Markdown',
                                reply_markup=markup)
    except Exception as ex:
        print(f"[COMMAND] Error {ex}")
