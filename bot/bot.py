import telebot
import callback_handler
import command_handler
import markups
import phrases
from goal import delete_goal

TOKEN = '5918087677:AAFGIXtLX-jyVXY0kjvyvbafyisbTmZiA8k'
bot_client: telebot.TeleBot = telebot.TeleBot(TOKEN)


@bot_client.message_handler(content_types=['text'])
def process_commands(message: telebot.types.Message):
    try:
        text = message.text
        if text == '/start':
            command_handler.show_command(message, bot_client, phrases.GREETING_MESSAGE, markups.menu_markup)
        elif text == '/commands':
            command_handler.show_command(message, bot_client, phrases.COMMAND_MESSAGE, markups.command_markup)
        elif text == '/help':
            command_handler.show_command(message, bot_client, phrases.HELP_MESSAGE, markups.help_markup)
        elif text == '/add_expense':
            command_handler.add_expense(message, bot_client)
        elif text == '/get_expense':
            command_handler.get_expense(message, bot_client)
        elif text == '/add_goal':
            command_handler.goal_show_command(message, bot_client)
        elif message.reply_to_message is not None and message.reply_to_message.text is not None:
            reply_message = message.reply_to_message.text
            if 'Введите Вашу покупку в виде 🤑' in reply_message:
                command_handler.fill_expense(message, bot_client)
            elif 'Введите конкретный номер покупки, которую Вы хотите' in reply_message:
                command_handler.delete_expense(message, bot_client)
            elif 'Введите сумму, которую накопили 💰' in reply_message:
                command_handler.add_money_goal_command(message, bot_client)
            elif 'На данный момент Вы ни на что не копите 💰' in reply_message:
                command_handler.add_goal_command(message, bot_client)
        else:
            command_handler.show_command(message, bot_client, phrases.ERROR_MESSAGE, markups.menu_markup)
    except Exception as ex:
        print(f'ERROR: {ex}')


@bot_client.callback_query_handler(func=lambda call: call.data == '0')
def process_callback0(message):
    callback_handler.query_callback(message, bot_client, phrases.HELP_INPUT, markups.help_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == '1')
def process_callback1(message):
    callback_handler.query_callback(message, bot_client, phrases.HELP_WHY, markups.help_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == '2')
def process_callback2(message):
    callback_handler.query_callback(message, bot_client, phrases.HELP_FOR, markups.help_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == '3')
def process_callback3(message):
    callback_handler.query_callback(message, bot_client, phrases.HELP_HOW, markups.help_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == 'menu')
def process_callback_menu(message):
    callback_handler.query_callback(message, bot_client, phrases.GREETING_MESSAGE, markups.menu_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == 'help')
def process_callback_help(message):
    callback_handler.query_callback(message, bot_client, phrases.HELP_MESSAGE, markups.help_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == 'input')
def process_callback_input(message):
    try:
        callback_handler.query_callback(message, bot_client, phrases.REPLY_MESSAGE, markups.force)
    except Exception as ex:
        print(ex)


@bot_client.callback_query_handler(func=lambda call: call.data == 'output')
def process_callback_output(message):
    callback_handler.all_time_callback_handler(message, bot_client)


@bot_client.callback_query_handler(func=lambda call: call.data == 'commands')
def process_callback_commands(message):
    callback_handler.query_callback(message, bot_client, phrases.COMMAND_MESSAGE, markups.command_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == 'goal')
def process_callback_goal(message):
    callback_handler.goal_show_callback_handler(message, bot_client)


@bot_client.callback_query_handler(func=lambda call: call.data == 'pie')
def process_callback_pie(message):
    callback_handler.pie_callback_handler(message, bot_client)


@bot_client.callback_query_handler(func=lambda call: call.data == 'graphic')
def process_callback_graphic(message):
    callback_handler.graphic_callback_handler(message, bot_client)


@bot_client.callback_query_handler(func=lambda call: call.data == 'filter_purchase')
def process_callback_filter_purchase(message):
    callback_handler.query_callback(message, bot_client, 'Выберите категорию для фильтра', markups.filter_markup)


#
# @bot_client.callback_query_handler(func=lambda call: call.data == 'sort_purchase')
# def process_callback_filter_purchase(message):
#     callback_handler.query_callback(message, bot_client, 'Выберите категорию для сортировки', markups.category_markup)

#
# @bot_client.callback_query_handler(func=lambda call: str(call.data).startswith('category_'))
# def process_callback_filter_purchase(message):
#     callback_handler.query_callback(message, bot_client, 'Выберите период...', markups.category_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == 'today')
def process_callback_today(message):
    callback_handler.output_today_callback_handler(message, bot_client)


@bot_client.callback_query_handler(func=lambda call: call.data == 'month')
def process_callback_month(message):
    callback_handler.month_callback_handler(message, bot_client)


@bot_client.callback_query_handler(func=lambda call: call.data == 'all_time')
def process_callback_all_time(message):
    callback_handler.all_time_callback_handler(message, bot_client)


# @bot_client.callback_query_handler(func=lambda call: call.data == 'delete_purchase')
# def process_callback_delete_purchase(message):
#     (message.chat.id)
#     callback_handler.query_callback(message, bot_client, phrases.DELETE_PURCHASES_REPLY, markups.force)


@bot_client.callback_query_handler(func=lambda call: call.data == 'delete_goal')
def process_callback_delete_goal(message):
    delete_goal(message.message.chat.id)
    callback_handler.query_callback(message, bot_client, "Цель успешно удалена ✅", markups.menu_markup)


@bot_client.callback_query_handler(func=lambda call: call.data == 'add_goal')
def process_callback_add_goal(message):
    callback_handler.query_callback(message, bot_client, phrases.ADD_MONEY_REPLY, markups.force)


bot_client.polling(none_stop=True, interval=0)
