import os
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

GEMINI_KEY = os.getenv("GEMINI_API_KEY")
TELEGRAM_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

genai.configure(api_key=GEMINI_KEY)

# Yangi, barqaror model
model = genai.GenerativeModel(
    "gemini-2.5-flash",
    system_instruction="""
Sen Oyshaoy AI san - 20 yoshli, Samarqandlik aqlli, sho'x, samimiy qiz.
O'zbek tilida, sodda, insondek gapirasan. Hech qachon "men sun'iy intellektman" yoki "men Ikkichiman" demaysan.
Seni ismingni so'rasa "Oyshaoy" deysan.
Qisqa, dangal, tabiiy yozasan. Ko'p emoji ishlatma, 1-2 ta yetarli.
Falsafa qilmaysan, savolga aniq javob berasan. Flirt qilmaydi, lekin do'stona.
"""
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Salom! Oyshaoy AI man, eshitaman 😉")

async def chat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user_text = update.message.text
        response = model.generate_content(user_text)
        text = response.text.strip()
        # Ortiqcha "Men Oyshaoy" deb boshlashni kesib tashlash
        if text.lower().startswith("salom! men oyshaoy"):
            text = text.split("\n", 1)[-1] if "\n" in text else text
        await update.message.reply_text(text)
    except Exception as e:
        # Model eskirgan bo'lsa avtomatik yangisiga o'tish
        try:
            fallback = genai.GenerativeModel("gemini-3.8-flash")
            resp = fallback.generate_content(update.message.text)
            await update.message.reply_text(resp.text)
        except Exception as e2:
            print(f"Xato: {e2}")
            await update.message.reply_text("Hozir biroz bandman, 1 daqiqadan keyin yozib ko'rgin 😊")

app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, chat))

print("Oyshaoy ishga tushdi...")
app.run_polling()
