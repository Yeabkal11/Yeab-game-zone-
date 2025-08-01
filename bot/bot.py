import asyncio
import os
import logging
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)
from api.main import update_queue # Import the shared queue
from .handlers import (
    start,
    play_command_handler,
    handle_button_press,
    handle_custom_amount,
)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")

async def main():
    """Start the bot."""
    # In a production environment using webhooks, the Application is built differently.
    # We use a shared queue to pass updates from the FastAPI app to the python-telegram-bot application.
    application = (
        Application.builder()
        .token(TELEGRAM_BOT_TOKEN)
        .updater(None) # Disable the internal updater
        .build()
    )

    # on different commands - answer in Telegram
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("play", play_command_handler))
    application.add_handler(CallbackQueryHandler(handle_button_press))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_custom_amount))


    # Set the webhook
    await application.bot.set_webhook(url=f"{WEBHOOK_URL}/api/telegram/webhook")

    # Run the bot until the user presses Ctrl-C
    # We process updates from the queue populated by the FastAPI webhook endpoint.
    async with application:
        while True:
            update = await update_queue.get()
            await application.process_update(update)

if __name__ == "__main__":
    # Note: This script is intended to be run as a Render Background Worker.
    # The FastAPI web service will run separately.
    logger.info("Starting bot worker...")
    asyncio.run(main())