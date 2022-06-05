import telebot
from extentions import ConvException, ConvertValute
from configs import TOKEN, keys


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands = ['start', 'help'])
def help(message: telebot.types.Message):

    text = 'Введите команду в формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество первой валюты>\nПример:\n\
доллар рубль 100\n\
Доступные валюты: /values'

    bot.reply_to(message, text)


@bot.message_handler(commands = ['values'])
def values(message: telebot.types.Message):

    text = 'Доступные валюты:'

    for i in keys.keys():
        text = '\n'.join((text, i))

    bot.reply_to(message, text)


@bot.message_handler(content_types = ['text'] )
def convert(message: telebot.types.Message):

    values = message.text.lower().split(' ')

    try:
        if len(values) != 3:
            raise ConvException('Неправильное количество параметров.')
        base, quote, amount = values
        result = ConvertValute.get_price(base, quote, amount)

    except ConvException as e:
        bot.reply_to(message, f'Ошибка\n{e}')

    except Exception as e:
        bot.reply_to(message, f'Ошибка на сервере, попробуйте снова\n{e}')

    else:
        text = f'{amount} {base} = {result} {quote}'
        bot.reply_to(message, text)


bot.polling()
