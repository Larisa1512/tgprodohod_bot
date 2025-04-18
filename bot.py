import os
from telegram import Bot
from telegram.ext import CommandHandler, Updater

# Получаем токен из переменных окружения
TOKEN = os.environ.get("TELEGRAM_TOKEN")
bot = Bot(token=TOKEN)

# Создаём объект Updater
updater = Updater(token=TOKEN, use_context=True)
dispatcher = updater.dispatcher

# ==== Работа с подписчиками ====
subscribers = set()

# Загружаем список подписчиков из файла
def load_subscribers():
    if os.path.exists("subscribers.txt"):
        with open("subscribers.txt", "r") as file:
            return set(int(line.strip()) for line in file.readlines())
    return set()

# Сохраняем нового подписчика в файл
def save_subscriber(chat_id):
    with open("subscribers.txt", "a") as file:
        file.write(f"{chat_id}\n")

subscribers = load_subscribers()

# ==== Команды ====

# /start — добавляет пользователя в список
def start(update, context):
    chat_id = update.effective_chat.id
    if chat_id not in subscribers:
        subscribers.add(chat_id)
        save_subscriber(chat_id)
        context.bot.send_message(chat_id=chat_id, text="✅ Вы подписались на рассылку!")
    else:
        context.bot.send_message(chat_id=chat_id, text="Вы уже подписаны 😉")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

# ==== Webhook (это нужно для Render) ====

updater.start_webhook(
    listen="0.0.0.0",  # Слушаем на всех интерфейсах
    port=int(os.environ.get('PORT', 5000)),  # Порт для Render (по умолчанию 5000)
    url_path=TOKEN,  # Токен будет частью URL
    webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}",  # URL Webhook для Render
)

updater.idle()

