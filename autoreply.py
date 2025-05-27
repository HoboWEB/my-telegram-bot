from telethon.sync import TelegramClient
from telethon.events import NewMessage
import random
import asyncio
from flask import Flask
from threading import Thread
import os

# --- 1. Настройка Flask для Render ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Автоответчик активен! Проверьте Telegram."

def run_flask():
    app.run(host='0.0.0.0', port=10000)  # Обязательные параметры для Render

# --- 2. Основной код бота ---
# Переносим конфигурацию в переменные окружения (безопасность!)
api_id = int(os.getenv('API_ID', 23495117))  # Значение по умолчанию можно удалить
api_hash = os.getenv('API_HASH', '97ec922bd7967ef76546b81a02bfd059')
phone = os.getenv('PHONE', '+79292020876')
contact = int(os.getenv('CONTACT', 1887931609))

# Счётчик сообщений от контакта
message_counter = 0

# Списки ответов
general_replies = [
    "Да, точняк!",
    "Ну и ну...",
    "Ну надо же!",
    "Как интересно!",
    "Жесть!"
]

question_replies = [
    "Надо подумать...",
    "Интересный вопрос!",
    "Да фиг его знает.",
    "Не уверен.",
    "Надо время обдумать."
]

async def run_bot():
    global message_counter
    client = TelegramClient('session_name', api_id, api_hash)
    
    @client.on(NewMessage(from_users=contact))
    async def reply(event):
        global message_counter
        message_counter += 1
        
        if message_counter % 2 == 0:
            if "?" in event.text:
                response = random.choice(question_replies)
            else:
                response = random.choice(general_replies)
            
            await asyncio.sleep(random.randint(5, 30))
            await event.reply(response)
            print(f"[Ответил] {response}")

    await client.start(phone)
    print("Автоответчик активен.")
    await client.run_until_disconnected()

# --- 3. Запуск в параллельных потоках ---
if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    # Запускаем бота в основном потоке
    asyncio.run(run_bot())
