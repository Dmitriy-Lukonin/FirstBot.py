import telebot
from config import token
from extensions import ConvertionException, CryptoConverter


bot = telebot.TeleBot(token)


@bot.message_handler(commands=['start'])
def start_command(message):
    bot.send_message(
        message.chat.id,
        'Привет! Я могу конвертировать валюты.\n' +
        'Чтобы получить помощь нажмите /help.'
    )


@bot.message_handler(commands=['help'])
def help_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.add(
        telebot.types.InlineKeyboardButton(
            'Напишите разработчику', url='https://t.me/Lukonin_Dmitriy'
        )
    )
    bot.send_message(
        message.chat.id,
        '1) Для получения списка доступных валют нажмите /values.\n' +
        '2) Для конвертации введите команду в формате:\n' +
        '<Валюта продажи> <Валюта Покупки> <Количество валюты продажи>\n' +
        'Пример ввода: Рубль Доллар 100\n' +
        '3) В ответе придет сообщение в следующем формате:\n' +
        'Валюта продажи: Рубль, сумма:  100\n' +
        'Валюта покупки: Доллар, сумма: 1.59\n',
        reply_markup=keyboard
    )


# Блок нужно доработать:
# 1. Сделать кнопки функциональными;
# 2. Кнопки создавать через цикл используя список валют keys
# (Можно будет прописать валюты российский рубль, белорусский рубль, доллар США)
@bot.message_handler(commands=['values'])
def values_command(message):
    keyboard = telebot.types.InlineKeyboardMarkup()
    keyboard.row(
        telebot.types.InlineKeyboardButton('BTC - Биткоин', callback_data='BTC')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('EUR - Евро', callback_data='EUR'),
        telebot.types.InlineKeyboardButton('USD - Доллар', callback_data='USD')
    )
    keyboard.row(
        telebot.types.InlineKeyboardButton('RUB - Рубль', callback_data='RUB'),
        telebot.types.InlineKeyboardButton('KZT - Тенге', callback_data='KZT')
    )

    bot.send_message(
        message.chat.id,
        'Валюты доступные для конвертации:',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):

    try:
        values = message.text.split(' ')
        if len(values) != 3:
            raise ConvertionException(f'Проверьте параметры ввода')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Команда мне не знакома\n{e}')
    else:

        text = f'Валюта продажи: {quote}, сумма: {amount} \n'\
               f'Валюта покупки: {base}, сумма: {total_base} '
        bot.send_message(message.chat.id, text)


bot.polling()
