import os
import json
from telegram import Bot, Update
from telegram.ext import CommandHandler, Updater, CallbackContext

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")

bot = Bot(token=TOKEN)
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Файл, где будем хранить ID пользователей
USERS_FILE = "users.json"

# Функция: сохранить ID пользователя
def save_user(user_id):
    try:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as file:
                users = json.load(file)
        else:
            users = []

        if user_id not in users:
            users.append(user_id)
            with open(USERS_FILE, "w") as file:
                json.dump(users, file)
    except Exception as e:
        print(f"Ошибка при сохранении пользователя: {e}")

# Команда /start
def start(update: Update, context: CallbackContext):
    user_id = update.effective_chat.id
    save_user(user_id)
    context.bot.send_message(chat_id=user_id, text="Вы подписались на рассылку ✅")

# Добавляем обработчик команды
start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# Запуск бота
updater.start_polling()
updater.idle()

