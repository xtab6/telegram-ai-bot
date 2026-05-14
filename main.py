from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("AIzaSyCSJJljD58LVxNEd0DHl8P6GFJWNMGPi_s"))

model = genai.GenerativeModel("8473059644:AAFmUUlHIgr5urBR-_YyEm7uxp0kMcfoHgA")

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    response = model.generate_content(text)

    await update.message.reply_text(response.text)

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply))

print("Bot running...")

app.run_polling()
