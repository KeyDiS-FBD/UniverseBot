import telebot
import requests
import wikikross
from urllib.parse import quote


file_of_results = open('result.txt')
bot = telebot.TeleBot('1001322227:AAF60A1WS4k41SS7CrQMxrFC5Oc4DLRVo3w')

#@bot.message_handler(content_types = ['rules'])

def send_rules(message):
    list_of_rules = wikikross.get_rules()
    bot.send_message(message.chat.id, list_of_rules)


#@bot.message_handler(content_types = ['start'])

def start_game(message):
    num_of_line = 0
    wikikross.send_results('https://ru.wikipedia.org/wiki/' + quote('Заглавная страница'))
    list_of_results, num_of_line = wikikross.print_line(num_of_line)
    bot.send_message(message.chat.id, list_of_results)


@bot.message_handler(content_types = ['text'])

def check_response_code(message):
    if(message.text == '/rules'):
        send_rules(message)
        return
    if(message.text == '/start'):
        start_game(message)
        return
    if(message.text == 'next'):
        list_of_results, num_of_line = wikikross.print_line(num_of_line)
        return
    page = 'https://ru.wikipedia.org/wiki/' + quote(message.text)
    response = requests.get(page)
    if(response.status_code == 200):
        max_of_line = wikikross.send_results(page)
        num_of_line = 0
        list_of_results, num_of_line = wikikross.print_line(num_of_line)
#        for results in dict_of_results.values():
#        bot.send_message(message.chat.id, results)
        bot.send_message(message.chat.id, list_of_results)
    else:
        bot.send_message(message.chat.id, 'Page not found')


bot.polling(none_stop = True, interval = 0)
