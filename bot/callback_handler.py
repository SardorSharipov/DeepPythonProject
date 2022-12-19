import datetime
import os.path

import telebot

import markups
import phrases
from analysis import pie_analysis, graphic_analysis
from goal import has_goal, read_goal
from purchase_info import PURCHASE_PATH, read_purchase, PurchaseInfo, purchase_to_str


def query_callback(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot, text: str, markup):
    try:
        bot_client.answer_callback_query(e.id)
        bot_client.send_message(chat_id=e.message.chat.id,
                                text=text,
                                parse_mode='Markdown',
                                reply_markup=markup)
    except:
        print("[Markup] Error")


def pie_callback_handler(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot):
    try:
        bot_client.answer_callback_query(e.id)
        purchases = read_purchase(e.message.chat.id)
        pie_analysis(purchases, e.message.chat.id)
        if os.path.exists(f'data/pies/{e.message.chat.id}.png'):
            bot_client.send_photo(
                chat_id=e.message.chat.id,
                photo=open(f'data/pies/{e.message.chat.id}.png', 'rb'),
                caption="Вот *Круговая Диаграмма* Ваших расходов по категориям:",
                parse_mode='Markdown'
            )
    except Exception as ex:
        print(f"[Markup] Error {ex}")


def graphic_callback_handler(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot):
    try:
        bot_client.answer_callback_query(e.id)
        purchases = read_purchase(e.message.chat.id)
        graphic_analysis(purchases, e.message.chat.id)
        print(os.path.exists(f'data/graphics/{e.message.chat.id}.png'))
        if os.path.exists(f'data/graphics/{e.message.chat.id}.png'):
            bot_client.send_photo(
                chat_id=e.message.chat.id,
                photo=open(f'data/graphics/{e.message.chat.id}.png', 'rb'),
                caption="Вот *График* Ваших расходов по датам:",
                parse_mode='Markdown'
            )
    except Exception as ex:
        print(f"[Markup] Error {ex}")


def goal_show_callback_handler(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot):
    try:
        if not has_goal(e.message.chat.id):
            bot_client.send_message(chat_id=e.message.chat.id,
                                    text=phrases.NO_GOAL_REPLY,
                                    parse_mode='Markdown',
                                    reply_markup=markups.force)
        else:
            goal = read_goal(e.message.chat.id)
            text = f"*На данный момент Вы копите на {goal.name}* 💸\n\n" + \
                   f"До цели ➡ *{goal.price} {goal.currency}*"
            bot_client.send_message(chat_id=e.message.chat.id,
                                    text=text,
                                    parse_mode='Markdown',
                                    reply_markup=markups.goal_markup)
    except Exception:
        print("[Markup] Error")


def message_output(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot, func, output_type: str):
    try:
        if os.path.exists(f'{PURCHASE_PATH}/{e.message.chat.id}.json'):
            purchases = read_purchase(e.message.chat.id)
            print(purchases)
            purchases_today = list(filter(func, purchases))
            if len(purchases_today):
                text = purchase_to_str(purchases_today)
                text = f"*Ваши покупки вида за {output_type} 📝:*\n" + \
                       "_Название Цена Валюта Категория Дата_\n\n" + \
                       text
                bot_client.send_message(chat_id=e.message.chat.id,
                                        text=text,
                                        parse_mode='Markdown',
                                        reply_markup=markups.analysis_markup)
            else:
                text = f"*Хм, произошла ошибочка 🤨*\n" + \
                       f"*Похоже, у Вас нет покупок за {output_type} 📝*\n\n" + \
                       f"Попробуйте воспользоваться командой /add\\_expense, чтобы их добавить 🙃"
                bot_client.send_message(chat_id=e.message.chat.id,
                                        text=text,
                                        parse_mode='Markdown',
                                        reply_markup=markups.menu_markup)
        else:
            bot_client.send_message(chat_id=e.message.chat.id,
                                    text=phrases.NO_JSON_MESSAGE,
                                    parse_mode='Markdown',
                                    reply_markup=markups.menu_markup)

    except Exception as ex:
        print(f"[Markup] Error {ex}")


def output_today_callback_handler(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot):
    def check_today(purchase: PurchaseInfo):
        return purchase.date.month == datetime.datetime.today().month and \
               purchase.date.year == datetime.datetime.today().year and \
               purchase.date.day == datetime.datetime.today().day

    message_output(e, bot_client, check_today, 'сегодня')


def month_callback_handler(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot):
    def check_month(purchase: PurchaseInfo):
        return purchase.date.month == datetime.datetime.today().month and \
               purchase.date.year == datetime.datetime.today().year

    message_output(e, bot_client, check_month, 'этот месяц')


def all_time_callback_handler(e: telebot.types.CallbackQuery, bot_client: telebot.TeleBot):
    def check_all(_: PurchaseInfo):
        return True

    message_output(e, bot_client, check_all, 'все время')
