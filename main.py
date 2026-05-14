from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

import google.generativeai as genai
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

model = genai.GenerativeModel("gemini-2.0-flash")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        response = model.generate_content(text)

        await update.message.reply_text(response.text)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(str(e))

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

print("Bot running...")

app.run_polling()
