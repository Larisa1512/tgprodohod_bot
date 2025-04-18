import os
from telegram import Bot
from telegram.ext import CommandHandler, Updater

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Команда /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Привет! Это бот для рассылки.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Запуск бота
updater.start_polling()
updater.idle()


