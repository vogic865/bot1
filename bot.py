import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Применяем патч для asyncio
nest_asyncio.apply()

# === Настройки ===
BOT_TOKEN = '7714387405:AAEaeoA0nwiHkj7uRKXI1jzoHbDW0BAYEQM'
SOURCE_CHANNEL_ID = -1002392464060  # ID исходного канала
TARGET_CHAT_IDS = [
    -1002644440071,   # Канал 1
    269504433         # Чат
]
MY_USER_ID = 269504433  # Твой ID для проверки

# === Обработчик новых сообщений в канале и личных сообщений ===
async def forward_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.channel_post:  # Это пост из канала
        if update.channel_post.chat.id == SOURCE_CHANNEL_ID:
            print("✅ Это нужный канал. Пересылаю сообщение во все целевые чаты...")
            message_id = update.channel_post.message_id
            from_chat_id = update.channel_post.chat.id

            for chat_id in TARGET_CHAT_IDS:
                try:
                    await context.bot.forward_message(
                        chat_id=chat_id,
                        from_chat_id=from_chat_id,
                        message_id=message_id
                    )
                    print(f"✅ Сообщение переслано в {chat_id}")

                    # Отправляем уведомление тебе
                    try:
                        await context.bot.send_message(
                            chat_id=MY_USER_ID,
                            text=f"✅ Сообщение из канала {from_chat_id} успешно переслано в {chat_id} (ID сообщения: {message_id})"
                        )
                    except Exception as e:
                        print(f"❌ Не удалось отправить уведомление пользователю: {e}")

                except Exception as e:
                    print(f"❌ Не удалось переслать в {chat_id}: {e}")
        else:
            print("⚠️ Сообщение из неизвестного канала")
    else:  # Это обычное сообщение (не из канала)
        user_id = update.effective_user.id
        if user_id != MY_USER_ID:
            print(f"🚫 Сообщение от неизвестного пользователя {user_id}. Игнорируем.")
            return

        print(f"📩 Получено личное сообщение от {update.effective_user.name}: {update.message.text}")

# === Отправка приветственного сообщения при запуске ===
async def post_init(app):
    try:
        await app.bot.send_message(chat_id=MY_USER_ID, text="✅ Бот запущен и готов к работе!")
        print("✅ Приветственное сообщение отправлено пользователю.")
    except Exception as e:
        print(f"❌ Не удалось отправить приветствие: {e}")

# === Основная функция запуска бота ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(MessageHandler(filters.ALL, forward_post))
    print("Бот запущен и ожидает новые посты...")
    await app.run_polling()

# Запуск
if __name__ == '__main__':
    asyncio.run(main())
