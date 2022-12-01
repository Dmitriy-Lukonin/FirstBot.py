import telebot
from config import keys, token
from utils import ConvertionException, CryptoConverter

bot = telebot.TeleBot(token)

# Блок работает
@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = 'Привет, я умею конвертировать валюты.\
Введи команду в следующем формате:\
n<Валюта>\
<В какую валюту необходимо перевести>\
<Количество>\n Список валют: /values'
    bot.reply_to(message, text)


# Блок работает
@bot.message_handler(commands=['values'])
def help(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key,))
    bot.reply_to(message, text)


# Блок работает
@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = message.text.split(' ')

    # сомнительное такое условие для американского доллара к тому же не работает
    if len(values) != 3:
        raise ConvertionException(f'Проверьте параметры ввода')

    quote, base, amount = values
    total_base = CryptoConverter.convert(quote, base, amount)

    text = f'Цена {amount} {quote} в {base} - {total_base}'
    bot.send_message(message.chat.id, text)


bot.polling()

# Git не могу настроить VCS