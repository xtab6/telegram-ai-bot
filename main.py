from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    MessageHandler,
    filters,
    ContextTypes,
)

from openai import OpenAI
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

async def reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        completion = client.chat.completions.create(
            model="openai/gpt-4o-mini",
            messages=[
                {"role": "user", "content": text}
            ]
        )

        answer = completion.choices[0].message.content

        await update.message.reply_text(answer)

    except Exception as e:
        print("ERROR:", e)
        await update.message.reply_text(str(e))

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(
    MessageHandler(filters.TEXT & ~filters.COMMAND, reply)
)

print("Bot running...")

app.run_polling()
