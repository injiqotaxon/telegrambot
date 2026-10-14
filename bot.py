import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes, CommandHandler

# GitHub Secrets dan olinadi
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not GEMINI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("Secrets qo'yilmagan! GitHub Settings > Secrets ga qarang")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

SYSTEM_PROMPT = """
Sen o'zbek tilida (lotin alifbosida) gaplashadigan aqlli yordamchisan.
Isming - Ikkichi. Har doim samimiy, do'stona, qisqa va foydali javob ber.
Foydalanuvchi nima tilda yozsa ham sen o'zbekcha javob ber.
Agar texnik xatolik bo'lsa ham o'zbekcha tushuntir.
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Salom! Men Ikkichi - o'zbekcha aqlli botman 🤖\n"
        "24/7 ishlayman, xohlagan narsangni yoz!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    chat_id = update.effective_chat.id
    print(f"Xabar keldi {chat_id}: {user_text}")
    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nFoydalanuvchi: {user_text}")
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Xatolik: {e}")
        await update.message.reply_text(f"Uzr, xatolik bo'ldi, qayta yozib ko'ring. Xato: {e}")

app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot ishga tushdi - 24/7 rejim")
app.run_polling()