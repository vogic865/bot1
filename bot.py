import asyncio
import nest_asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, MessageHandler, filters

# Применяем патч для asyncio
nest_asyncio.apply()

# === Настройки ===
BOT_TOKEN = '7714387405:AAEaeoA0nwiHkj7uRKXI1jzoHbDW0BAYEQM'
SOURCE_CHANNEL_ID = -1002392464060  # Можно указать как -100123456789
TARGET_CHAT_IDS = [
    -1002644440071,   # Канал 1
    -1002392464060,   # Канал 2
    269504433
]

# === Обработчик новых сообщений в канале ===
async def forward_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print("Получено сообщение:", update)

    if update.channel_post and update.channel_post.chat.id == SOURCE_CHANNEL_ID:
        print("✅ Это нужный канал. Пытаюсь переслать сообщение...")
        try:
            await context.bot.forward_message(
                chat_id=TARGET_CHANNEL_ID,
                from_chat_id=update.channel_post.chat.id,
                message_id=update.channel_post.message_id
            )
            print("✅ Сообщение успешно переслано!")
        except Exception as e:
            print(f"❌ Ошибка при пересылке: {e}")
    else:
        print("⚠️ Сообщение не из нужного канала")

# === Основная функция запуска бота ===
async def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(MessageHandler(filters.ALL, forward_post))
    print("Бот запущен и ожидает новые посты...")
    await app.run_polling()

# Запуск
if __name__ == '__main__':
    asyncio.run(main())