import telebot

# Вставь сюда свой токен бота
TOKEN = "ТВОЙ_ТОКЕН_БОТА"
bot = telebot.TeleBot(TOKEN)

# Команда /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to Altarion RPG Bot!")

# Эхо-сообщение (повторяет всё, что пишет пользователь)
@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.reply_to(message, message.text)

# Запуск бота
bot.polling()
