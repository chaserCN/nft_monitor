"""Helper script to get chat ID of a group/channel."""
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes
import os
from dotenv import load_dotenv

load_dotenv()

async def get_chat_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Print chat ID when bot receives any message."""
    chat = update.effective_chat

    print("\n" + "="*60)
    print("CHAT INFO")
    print("="*60)
    print(f"Chat ID: {chat.id}")
    print(f"Chat Type: {chat.type}")
    print(f"Chat Title: {chat.title}")
    print("="*60)
    print(f"\nAdd this to your .env file:")
    print(f"TELEGRAM_CHANNEL_ID={chat.id}")
    print("="*60)

    await update.message.reply_text(
        f"✅ Chat ID obtained!\n\n"
        f"Chat ID: `{chat.id}`\n"
        f"Type: {chat.type}\n"
        f"Title: {chat.title}\n\n"
        f"Add this bot as admin to post messages!",
        parse_mode='Markdown'
    )

def main():
    """Run the bot."""
    token = os.getenv('TELEGRAM_BOT_TOKEN')

    if not token:
        print("❌ TELEGRAM_BOT_TOKEN not found in .env")
        return

    print("🤖 Bot started!")
    print("\nSteps:")
    print("1. Add this bot to your group/channel as admin")
    print("2. Send any message to the group")
    print("3. The chat ID will be printed here\n")

    app = Application.builder().token(token).build()
    app.add_handler(MessageHandler(filters.ALL, get_chat_id))

    app.run_polling()

if __name__ == "__main__":
    main()
