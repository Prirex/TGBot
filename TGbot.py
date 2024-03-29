import telebot
from config import keys, TOKEN
from extensions import APIException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"]) # start help по какой команде запускаектся данный обработчик
def help(message: telebot.types.Message):
    text = "Чтобы начать работу введите команду боту в следюущем формате:\n <имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты> \n/values - список доступных валют"
    bot.reply_to(message, text)


@bot.message_handler(commands=["values"]) # values по какой команде запускаектся данный обработчик
def values (message: telebot.types.Message):
        text = "Доступные валюты: "
        for key in keys.keys():
            text = "\n".join((text, key, ))
        bot.reply_to(message, text)


@bot.message_handler(content_types=["text", ])
def convert(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) > 3:
            raise APIException("Слишком много параметров.")
        elif len(values) < 3:
            raise APIException("Мало параметров.")

        base, quote, amount = values
        total_base = CryptoConverter.convert(base, quote, amount)
    except APIException as e:
        bot.reply_to(message, f'Ошибка пользователя\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)

bot.polling()