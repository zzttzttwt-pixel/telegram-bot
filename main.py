import asyncio
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai

# إعداد السجلات (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# إعداد مفاتيح التشغيل من متغيرات البيئة (Environment Variables)
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# إعداد مكتبة Gemini
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro')

# دالة الترحيب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا بوت ذكاء اصطناعي مرتبط بـ Gemini. أرسل لي أي سؤال وسأجيبك فوراً.")

# دالة الرد على الرسائل باستخدام Gemini
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # إرسال النص إلى Gemini وجلب الرد
        response = model.generate_content(user_text)
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error calling Gemini API: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً.")

# بناء وتجهيز تطبيق التليجرام
application = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

# إضافة الأوامر والمستقبلات
application.add_handler(CommandHandler("start", start))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

# تشغيل البوت بالطريقة المتوافقة مع بايثون الحديث
if __name__ == "__main__":
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(application.run_polling())
