import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, PreCheckoutQueryHandler
from config import Config

try:
    from database import Database
    db = Database()
except:
    db = None

async def start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("📥 تحميل فيديو", callback_data="menu_download"),
         InlineKeyboardButton("🧠 ذكاء اصطناعي", callback_data="menu_ai")],
        [InlineKeyboardButton("💳 شحن رصيد", callback_data="menu_topup"),
         InlineKeyboardButton("👥 الإحالات", callback_data="menu_referral")],
    ])
    await update.message.reply_text(
        f"👋 أهلاً {user.first_name}!\n\n"
        f"🤖 بوت متعدد الخدمات\n"
        f"• 📥 تحميل يوتيوب وتيك توك\n"
        f"• 🧠 ذكاء اصطناعي",
        reply_markup=kb
    )

async def button_handler(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    if q.data == "menu_download":
        kb = InlineKeyboardMarkup([
            [InlineKeyboardButton("▶️ يوتيوب", callback_data="dl_youtube"),
             InlineKeyboardButton("🎵 تيك توك", callback_data="dl_tiktok")],
            [InlineKeyboardButton("🔙 رجوع", callback_data="back_main")],
        ])
        await q.edit_message_text("📥 أرسل رابط الفيديو بعد اختيار المنصة:", reply_markup=kb)
    elif q.data == "menu_ai":
        ctx.user_data["ai_mode"] = "chat"
        await q.edit_message_text("🧠 اكتب سؤالك وسأجيبك!\n\n💡 تكلفة: 1 نقطة لكل رسالة")
    elif q.data == "back_main":
        await start_from_callback(q, ctx)
    elif q.data.startswith("dl_"):
        ctx.user_data["download_mode"] = q.data.replace("dl_", "")
        await q.edit_message_text("📎 أرسل الرابط الآن:")

async def start_from_callback(q, ctx):
    kb = InlineKeyboardMarkup([
        [InlineKe
