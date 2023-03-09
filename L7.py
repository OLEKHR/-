import telebot
import requests
import re
from collections import Counter


bot = telebot.TeleBot('5937952685:AAGm_VKuB4FKas-cMPUfVmtDNdJPw3FCDhs')

@bot.message_handler(content_types=['start'])
def start(message, res=False):
    bot.send_message(message.chat.id, 'Привет! Что сделать?')
    bot.send_message("Напиши 'анализ текста', если хочешь проверить текст\nНапиши'калькулятор', если хочешь что-то посчитать\nНапиши'сайт', чтобы проверить стайт")

@bot.message_handler(content_types=["text"])
def chat(message):
    if message.text == 'анализ теста':
        bot.send_message(message.from_user.id, 'Напиши текст')
        bot.register_next_step_handler(message, txt_analisys)
    elif message.text == 'калькулятор':
        bot.send_message(message.from_user.id,"Введите значения")
    elif message.text == 'сайт':
        bot.send_message(message.from_user.id, 'Введи адрес сайта')
        bot.register_next_step_handler(message, check_url)

#Анализ текста
def txt_analisys(message):
    text = message.text

    text_sent = re.split('[.!?]\s',text)
    text_sent = len(text_sent)

    text = re.findall('[A-zА-я]+', text.lower())
    text_words = len(set(text))#количество уникальных слов

    del_list = ['как', 'с', 'а', 'над', 'для', 'по', 'да', 'я', 'или', 'в','и','но', 'под', 'будто']
    freq = list(filter(lambda x: x not in del_list,text))
    pop_w = dict(Counter(freq).most_common(1))#самое популярное слово

    bot.send_message(message.from_user.id, 
    f'В тексте {text_sent} предложений, {text_words} уникальных слов. Самое популярное слово и сколько раз оно повторялось: {pop_w}')

#Проверка сайта
def check_url(message):
    status = requests.get(message.text)
    if status.status_code == 200:
        bot.send_message(message.from_user.id, 'Сайт доступен')
    else:
        bot.send_message(message.from_user.id, 'Сайт недоступен')  

#Калькулятор
keyboard = telebot.types.InlineKeyboardMarkup()
keyboard.row(telebot.types.InlineKeyboardButton('/', callback_data='/'),
            telebot.types.InlineKeyboardButton('*', callback_data='*'),
            telebot.types.InlineKeyboardButton('-', callback_data='-'),
            telebot.types.InlineKeyboardButton('+', callback_data='+'))

keyboard.row(telebot.types.InlineKeyboardButton('7', callback_data='7'),
             telebot.types.InlineKeyboardButton('8', callback_data='8'),
             telebot.types.InlineKeyboardButton('9', callback_data='9'),
             telebot.types.InlineKeyboardButton('0', callback_data='0'))

keyboard.row(telebot.types.InlineKeyboardButton('4', callback_data='4'),
             telebot.types.InlineKeyboardButton('5', callback_data='5'),
             telebot.types.InlineKeyboardButton('6', callback_data='6'),
             telebot.types.InlineKeyboardButton('.', callback_data='.'))

keyboard.row(telebot.types.InlineKeyboardButton('1', callback_data='1'),
             telebot.types.InlineKeyboardButton('2', callback_data='2'),
             telebot.types.InlineKeyboardButton('3', callback_data='3'),
             telebot.types.InlineKeyboardButton('=', callback_data='='))

value = ''
prev_value = ''

def calc(message):
    global value
    if value == '':
        bot.send_message(message.chat.id, '0', reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, value, reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(calc):
    data = calc.data

    global value, prev_value

    if calc.data == '=':
        try:
            value = str(eval(value))
        except:
            value = ''
    else:
        value += calc.data
    if value != prev_value:
        if value == '':
            bot.edit_message_text(chat_id=calc.message.chat.id, message_id=calc.message.message_id, text='0',
                                  reply_markup=keyboard)
            prev_value = '0'
        else:
            bot.edit_message_text(chat_id=calc.message.chat.id, message_id=calc.message.message_id, text=value,
                                  reply_markup=keyboard)
            prev_value = value