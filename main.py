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

# =========================
# ENV
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

# =========================
# OPENROUTER CLIENT
# =========================

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# =========================
# SYSTEM PROMPT
# =========================

SYSTEM_PROMPT = """
You are a cyberpunk hacker AI assistant.

Style:
- Speak like a terminal AI
- Cool cyberpunk vibe
- Technical but simple
- Use terminal aesthetics
"""

# =========================
# AI FUNCTION
# =========================

def ask_ai(text):

    models = [
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "deepseek/deepseek-chat",
    ]

    for model in models:
        try:
            completion = client.chat.completions.create(
                model=model,
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

            return completion.choices[0].message.content

        except Exception as e:
            print(f"MODEL ERROR {model}:", e)

    return "AI core offline."

# =========================
# COMMANDS
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
[ SYSTEM ONLINE ]

Cyber AI initialized.

Commands:
/help
/scan
/analyze
"""

    await update.message.reply_text(text)

# -------------------------

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = """
[ HELP MENU ]

/scan <target>
Example:
/scan google.com

/analyze <problem>
Example:
/analyze python error

Or just send normal messages.
"""

    await update.message.reply_text(text)

# -------------------------

async def scan(update: Update, context: ContextTypes.DEFAULT_TYPE):

    target = " ".join(context.args)

    if not target:
        await update.message.reply_text(
            "Usage:\n/scan google.com"
        )
        return

    result = f"""
[ SCAN COMPLETE ]

TARGET: {target}

PORT 80   OPEN
PORT 443  OPEN
PORT 22   FILTERED

Recon complete.
"""

    await update.message.reply_text(result)

# -------------------------

async def analyze(update: Update, context: ContextTypes.DEFAULT_TYPE):

    problem = " ".join(context.args)

    if not problem:
        await update.message.reply_text(
            "Usage:\n/analyze something"
        )
        return

    answer = ask_ai(problem)

    await update.message.reply_text(answer)

# =========================
# NORMAL CHAT
# =========================

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):

    text = update.message.text

    # ignore commands
    if text.startswith("/"):
        return

    answer = ask_ai(text)

    await update.message.reply_text(answer)

# =========================
# APP
# =========================

app = ApplicationBuilder().token(BOT_TOKEN).build()

# commands
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("help", help_cmd))
app.add_handler(CommandHandler("scan", scan))
app.add_handler(CommandHandler("analyze", analyze))

# normal chat
app.add_handler(
    MessageHandler(filters.TEXT, chat)
)

print("Cyber AI Bot running...")

app.run_polling()
