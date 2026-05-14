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

Style:
- Speak like a terminal operator
- Use cyberpunk/hacker vibe
- Short technical responses
- Add terminal aesthetics when possible
"""

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
[ SYSTEM ONLINE ]

Available commands:
/scan
/analyze
/help

AI core initialized...
"""
    await update.message.reply_text(text)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = """
[ HELP MENU ]

/scan <target>
Example:
/scan google.com

/analyze <problem>
Example:
/analyze python error

Or send normal chat.
"""
    await update.message.reply_text(text)

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = " ".join(context.args)

    if not target:
        await update.message.reply_text(
            "Usage:\n/scan <target>"
        )
        return

    fake_result = f"""
[ SCANNING TARGET ]
TARGET: {target}

PORT 80  → OPEN
PORT 443 → OPEN

Reconnaissance complete.
"""

    await update.message.reply_text(fake_result)

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):
    problem = " ".join(context.args)

    if not problem:
        await update.message.reply_text(
            "Usage:\n/analyze <problem>"
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
                "content": f"Analyze this:\n{problem}"
            }
        ]
    )

    answer = completion.choices[0].message.content

    await update.message.reply_text(answer)

# =========================
# NORMAL CHAT
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

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
