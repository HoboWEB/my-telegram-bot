from telethon.sync import TelegramClient
from telethon.events import NewMessage
import random
import asyncio
from flask import Flask
from threading import Thread
import os

# 1. Настройка Flask (чтобы бот не "засыпал" на Render)
app = Flask(__name__)

@app.route('/')
def home():
    return "Бот активен! Проверьте Telegram."

def run_flask():
    app.run(host='0.0.0.0', port=10000)  # Render требует порт 10000

# 2. Настройки бота (берутся из переменных окружения Render)
api_id = int(os.getenv('API_ID'))        # Ваш API ID из my.telegram.org
api_hash = os.getenv('API_HASH')         # Ваш API HASH
phone = os.getenv('PHONE')               # Ваш номер: "+79292020876"
contact = int(os.getenv('CONTACT'))      # ID чата (цифры, а не @username)

# 3. Уникальное имя сессии для Render
session_name = 'render_session'  # Это создаст файл render_session.session

# 4. Списки ответов (можно менять)
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

# 5. Основная функция бота
async def run_bot():
    global message_counter
    message_counter = 0  # Счётчик сообщений
    
    client = TelegramClient(session_name, api_id, api_hash)
    
    # Обработчик новых сообщений
    @client.on(NewMessage(from_users=contact))
    async def reply(event):
        global message_counter
        message_counter += 1
        
        # Ответ каждое 2-е сообщение
        if message_counter % 2 == 0:
            if "?" in event.text:  # Если вопрос
                response = random.choice(question_replies)
            else:
                response = random.choice(general_replies)
            
            # Задержка для "естественности" (5-30 сек)
            await asyncio.sleep(random.randint(5, 30))
            await event.reply(response)
            print(f"[Ответил] {response}")

    # Запуск клиента
    print("Подключаемся к Telegram...")
    await client.start(phone)
    print("Автоответчик активен!")
    await client.run_until_disconnected()

# 6. Запуск Flask и бота в параллельных потоках
if __name__ == '__main__':
    # Запускаем Flask в отдельном потоке
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True  # Поток завершится при закрытии программы
    flask_thread.start()

    # Запускаем бота
    asyncio.run(run_bot())
