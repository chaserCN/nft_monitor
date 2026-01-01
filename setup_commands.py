"""Setup bot commands in Telegram."""
import asyncio
import os
from telegram import BotCommand
from telegram.ext import Application
from dotenv import load_dotenv

load_dotenv()


async def setup_commands():
    """Register bot commands with Telegram."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env")
        return

    # Define commands (Ukrainian language)
    commands = [
        BotCommand("start", "Початок роботи з ботом"),
        BotCommand("help", "Детальна довідка"),
        BotCommand("showall", "Показати всі доступні подарунки"),
        BotCommand("list", "Показати відстежувані пари"),
        BotCommand("add", "Додати пару для моніторингу"),
        BotCommand("delete", "Видалити пару з моніторингу"),
        BotCommand("setprice", "Встановити максимальну ціну"),
        BotCommand("setinterval", "Встановити інтервал перевірки"),
        BotCommand("pause", "Призупинити моніторинг"),
        BotCommand("resume", "Відновити моніторинг"),
        BotCommand("stats", "Переглянути статистику"),
        BotCommand("image", "Показати зображення подарунка"),
    ]

    # Create application
    app = Application.builder().token(token).build()

    # Set commands
    await app.bot.set_my_commands(commands)

    print("✅ Commands registered successfully!")
    print("\nRegistered commands:")
    for cmd in commands:
        print(f"  /{cmd.command} - {cmd.description}")

    # Stop application
    await app.shutdown()


if __name__ == "__main__":
    asyncio.run(setup_commands())
