from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
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

SYSTEM_PROMPT = """
You are a cyberpunk hacker AI assistant.
Speak like a cool terminal AI.
"""

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "[ SYSTEM ONLINE ]\nCyber AI ready."
    )

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "/scan <target>\n/analyze <problem>"
    )

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        target = " ".join(context.args)

        if not target:
            await update.message.reply_text(
                "Usage:\n/scan google.com"
            )
            return

        result = f"""
[ SCAN COMPLETE ]

TARGET: {target}

PORT 80  OPEN
PORT 443 OPEN
"""

        await update.message.reply_text(result)

    except Exception as e:
        print("SCAN ERROR:", e)

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = " ".join(context.args)

        if not text:
            await update.message.reply_text(
                "Usage:\n/analyze something"
            )
            return

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        answer = completion.choices[0].message.content

        await update.message.reply_text(answer)

    except Exception as e:
        print("ANALYZE ERROR:", e)
        await update.message.reply_text(str(e))

# =========================
# NORMAL CHAT
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text

        # skip command
        if text.startswith("/"):
            return

        completion = client.chat.completions.create(
            model="deepseek/deepseek-chat:free",
            messages=[
                {
                    "role": "system",
                    "content": SYSTEM_PROMPT
                },
                {
                    "role": "user",
                    "content": text
                }
            ]
        )

        answer = completion.choices[0].message.content

        await update.message.reply_text(answer)

    except Exception as e:
        print("CHAT ERROR:", e)
        await update.message.reply_text(str(e))

# =========================
# APP
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("analyze", analyze))

app.add_handler(
    MessageHandler(filters.TEXT, chat)
)

print("Cyber AI Bot running...")

app.run_polling()
