import os
from fastapi import FastAPI, Request, Response
import telegram
from telegram import Update
import asyncio

# This is a placeholder for your actual bot's update queue.
# In a real application, you'd get this from your bot instance.
# For now, we'll simulate it.
update_queue = asyncio.Queue()

app = FastAPI()

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telegram.Bot(token=BOT_TOKEN)

@app.get("/")
def read_root():
    return {"Status": "Yeab Game Zone API is running."}

@app.post("/api/telegram/webhook")
async def webhook(request: Request):
    """Handles incoming Telegram updates."""
    data = await request.json()
    update = Update.de_json(data, bot)
    await update_queue.put(update)
    return Response(status_code=200)

# The following is a simple Express-like server for Render's health checks.
# This part is more conceptual in a FastAPI context.
# Render will typically ping the root URL ("/").
# The JavaScript code from the prompt is not directly translatable to Python in this context,
# but the FastAPI root endpoint serves the same purpose.