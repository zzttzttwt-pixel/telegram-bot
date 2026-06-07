import os
import google.generativeai as genai
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")
GEMINI_KEY = os.getenv("GEMINI_API_KEY", "")

genai.configure(api_key=GEMINI_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="download"),
         InlineKeyboardButton("🧠 ذكاء اصطناعي", callback_data="ai")],
    ])
    await update.message.reply_text(
        f"👋 أهلاً {user.first_name}!\n\nاختر خدمة:",
        reply_markup=kb
    )

async def button(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "download":
        ctx.user_data["mode"] = "download"
        await q.edit_message_text("📎 أرسل رابط يوتيوب أو تيك توك:")
    elif q.data == "ai":
        ctx.user_data["mode"] = "ai"
        await q.edit_message_text("🧠 اكتب سؤالك:")

async def message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    mode = ctx.user_data.get("mode")
    text = update.message.text
    if mode == "ai":
        msg = await update.message.reply_text("⏳ جارٍ المعالجة...")
        try:
            res = model.generate_content(text)
            await msg.edit_text(res.text)
        except Exception as e:
            await msg.edit_text(f"❌ خطأ: {e}")
    elif mode == "download":
        msg = await update.message.reply_text("⏳ جارٍ التحميل...")
        try:
            import yt_dlp, tempfile
            with tempfile.TemporaryDirectory() as tmp:
                opts = {"outtmpl": f"{tmp}/video.%(ext)s", "format": "best[height<=480]", "quiet": True}
                with yt_dlp.YoutubeDL(opts) as ydl:
                    info = ydl.extract_info(text, download=True)
                    path = ydl.prepare_filename(info)
            await msg.delete()
            await update.message.reply_document(open(path, "rb"), caption=info.get("title",""))
        except Exception as e:
            await msg.edit_text(f"❌ {e}")
    else:
        await start(update, ctx)

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message))
    app.run_polling()

if __name__ == "__main__":
    main()
