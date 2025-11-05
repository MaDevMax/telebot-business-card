# My first Telegram bot
# Author: MaDevMax | 2025

import telebot
from datetime import datetime

# создаём экземпляр бота
bot = telebot.TeleBot("YOUR_TOKEN_HERE")  # сюда вставишь свой токен
ADMIN_ID = 12345689  # сюда подставишь свой ID, который узнаешь у @userinfobot

# запоминаем пользователей, которые хотят отправить сообщение
waiting_users = set()


@bot.message_handler(commands=['start'])
def start(message):
    """Приветственное сообщение и список команд"""
    text = (
        "Привет! 👋 Я первый бот MaDevMax.\n"
        "Вот что я умею:\n"
        "/about - немного обо мне\n"
        "/feedback - написать сообщение"
    )
    bot.send_message(message.chat.id, text)


@bot.message_handler(commands=['about'])
def about(message):
    """Информация об авторе"""
    bot.send_message(
        message.chat.id,
        "Я начинающий разработчик на Python. 😎\n"
        "Создаю Telegram‑ботов и системы автоматизации."
    )


@bot.message_handler(commands=['feedback'])
def ask_feedback(message):
    """Переход к отправке сообщения"""
    bot.send_message(message.chat.id, "✉️ Напиши сюда своё сообщение, я всё прочитаю.")
    waiting_users.add(message.chat.id)


@bot.message_handler(func=lambda m: m.chat.id in waiting_users)
def save_feedback(message):
    """Сохраняю обратную связь и отправляю админу"""
    waiting_users.discard(message.chat.id)

    # Отправить админу в Telegram
    bot.forward_message(ADMIN_ID, message.chat.id, message.message_id)

    # Записать в файл
    record = f"[{datetime.now()}] @{message.from_user.username}: {message.text}\n"
    with open("feedback.txt", "a", encoding="utf-8") as file:
        file.write(record)

    bot.send_message(message.chat.id, "✅ Спасибо! Сообщение отправлено.")


print("Бот MaDevMax запущен...")
bot.polling(none_stop=True)
