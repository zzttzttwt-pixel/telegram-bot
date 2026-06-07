import os
from google import genai
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# 1. ضع مفتاح الـ API الخاص بـ Gemini هنا
GEMINI_API_KEY = "ضع_مفتاح_جوجل_هنا"
# 2. ضع التوكن الخاص ببوت تليجرام (الذي أخذته من BotFather) هنا
TELEGRAM_BOT_TOKEN = "ضع_توكن_تليجرام_هنا"

# تهيئة عميل Gemini
client = genai.Client(api_key=GEMINI_API_KEY)

# دالة التعامل مع الرسائل القادمة من تليجرام
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_text = update.message.text # نص رسالة المستخدم
    
    try:
        # إرسال النص إلى نموذج Gemini 3.5 Flash السريع
        response = client.models.generate_content(
            model='gemini-3.5-flash',
            contents=user_text,
        )
        
        # إرسال رد Gemini إلى مستخدم تليجرام
        await update.message.reply_text(response.text)
        
    except Exception as e:
        await update.message.reply_text("عذرًا، حدث خطأ أثناء معالجة الطلب.")
        print(f"Error: {e}")

def main():
    # تشغيل بوت تليجرام
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # جعل البوت يستمع لجميع الرسائل النصية
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("البوت يعمل الآن ومربوط بـ Gemini...")
    import asyncio

if __name__ == "__main__":
    try:
        # لتجنب مشاكل الـ Event Loop في إصدارات بايثون الحديثة
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
    loop.run_until_complete(application.run_polling())
    

if __name__ == '__main__':
    main()
