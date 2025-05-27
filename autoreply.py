from telethon.sync import TelegramClient
from telethon.events import NewMessage
import random
import asyncio

# Ваши данные (замените!)
api_id = 23495117                   # Ваш API ID
api_hash = '97ec922bd7967ef76546b81a02bfd059' # Ваш API HASH
phone = '+79292020876'              # Ваш номер
contact = 844629954     # Или ID (через @userinfobot)

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

async def main():
    global message_counter
    client = TelegramClient('session_name', api_id, api_hash)
    
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
    await client.start(phone)
    print("Автоответчик активен. Нажмите Ctrl+C для остановки.")
    await client.run_until_disconnected()

if __name__ == '__main__':
    asyncio.run(main())
