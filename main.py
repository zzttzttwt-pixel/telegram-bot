import asyncio
import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from google import genai

# إعداد السجلات (Logging)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# جلب التوكن ومفتاح الذكاء الاصطناعي من السيرفر
TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# تشغيل مكتبة Gemini المحدثة تلقائياً
client = genai.Client(api_key=GEMINI_API_KEY)

# دالة الترحيب /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("أهلاً بك! أنا بوت ذكاء اصطناعي متاح لخدمتك. أرسل لي أي سؤال وسأجيبك فوراً.")

# دالة الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text
    try:
        # استخدام النظام الجديد لجوجل لطلب الإجابة
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=user_text,
        )
        await update.message.reply_text(response.text)
    except Exception as e:
        logging.error(f"Error calling Gemini API: {e}")
        await update.message.reply_text("عذراً، حدث خطأ أثناء معالجة طلبك. يرجى المحاولة لاحقاً.")

# التأكد من وجود التوكن قبل بناء التطبيق لمنع الانهيار
if not TELEGRAM_BOT_TOKEN:
    raise ValueError("خطأ: TELEGRAM_BOT_TOKEN غير موجود في متغيرات البيئة بـ Railway!")

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
