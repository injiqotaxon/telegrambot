import os
from google import genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

client = genai.Client(api_key=GEMINI_KEY)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom, men Oyshaoy 😉")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=f"""
Sen Oyshaoy AI san. 20 yoshli, Samarqandlik qizsan.
O'zbek tilida, qisqa, dangal, insondek gapir.
Hech qachon "men AI man", "men Ikkichiman" dema.
O'zingni maqtama, savolga to'g'ridan javob ber.
Kulgili, samimiy bo'l, 1 ta emoji yetarli.
Savol: {user_text}
"""
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        print(f"Xato: {e}")
        # Agar 2.5 ishlamasa, 3.8 ni sinaydi
        try:
            resp2 = client.models.generate_content(model="gemini-3.8-flash", contents=user_text)
            await update.message.reply_text(resp2.text)
        except Exception as e2:
            await update.message.reply_text(f"Bir soniya, xato: {e2}")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Oyshaoy ishga tushdi...")
app.run_polling()
