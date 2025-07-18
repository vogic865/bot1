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
    -1002392464060,   # Канал 2
    269504433         # Чат
]

# === Обработчик новых сообщений в канале ===
async def forward_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получено сообщение:", update)

    if update.channel_post and update.channel_post.chat.id == SOURCE_CHANNEL_ID:
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
            except Exception as e:
                print(f"❌ Не удалось переслать в {chat_id}: {e}")
    else:
        print("⚠️ Сообщение не из нужного канала или не channel_post")

# === Основная функция запуска бота ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_post))
    print("Бот запущен и ожидает новые посты...")
    await app.run_polling()

# Запуск
if __name__ == '__main__':
    asyncio.run(main())
