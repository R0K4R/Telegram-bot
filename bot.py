import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest
import yt_dlp

# --- زانیارییەکان لێرە بگۆڕە ---
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"
CHANNEL_ID = "@YourChannel"  # یوزەرنەیمی کەناڵەکەت لێرە دابنێ (@hamaesmael)
CHANNEL_URL = "https://t.me/hamaesmael" # لینکی کەناڵەکەت لێرە دابنێ
ADMIN_ID = 764898328  # ئایدی تێلێگرامی خۆت لێرە دابنێ بۆ ئەوەی ئامارەکان ببینی
# -------------------------

# فایلی پاشەکەوتکردنی بەکارهێنەران
USERS_FILE = "users.txt"

def add_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f: f.write("")
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

async def is_user_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)
    keyboard = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سڵاو! بۆ بەکارهێنانی بۆتەکە و داگرتنی ڤیدیۆ، پێویستە سەرەتا جۆینی کەناڵەکەمان بکەیت. 👇",
        reply_markup=reply_markup
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                count = len(f.read().splitlines())
            await update.message.reply_text(f"📊 ئاماری بۆتەکە:\n\nکۆی بەکارهێنەران: {count} کەس")
        else:
            await update.message.reply_text("هێشتا هیچ ئامارێک نییە.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ١. تەنها دەق (Text) وەردەگرێت، وێنە و ڤۆیس و ڤیدیۆ پشتگوێ دەخات
    if not update.message.text:
        return

    user_id = update.effective_user.id
    add_user(user_id)
    url = update.message.text

    # ٢. پشکنینی جۆینی ناچاری
    if not await is_user_member(update, context):
        keyboard = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "ببورە! بۆ ئەوەی بتوانیت ڤیدیۆ دابگریت، دەبێت سەرەتا جۆینی کەناڵەکەمان بکەیت. 👇",
            reply_markup=reply_markup
        )
        return

    # ٣. پشکنینی لینکەکان
    valid_sites = ["tiktok.com", "facebook.com", "fb.watch", "instagram.com", "instagr.am"]
    if not any(site in url for site in valid_sites):
        return

    msg = await update.message.reply_text("⏳ خەریکم ڤیدیۆکە ئامادە دەکەم... تکایە چاوەڕێبە.")
    file_path = f"vid_{user_id}.mp4"

    ydl_opts = {
        'format': 'best',
        'outtmpl': file_path,
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if os.path.exists(file_path):
            # دروستکردنی دوگمەی شەفاف بۆ زیادکردنی سەردانیکەر
            keyboard = [
                [InlineKeyboardButton("کەناڵی فەرمی ئێمە 📢", url=CHANNEL_URL)],
                [InlineKeyboardButton("ناردن بۆ هاوڕێیان 🚀", url=f"https://t.me/share/url?url={CHANNEL_URL}&text=باشترین%20بۆت%20بۆ%20داگرتنی%20ڤیدیۆ!%20🔥")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            with open(file_path, 'rb') as video:
                await update.message.reply_video(
                    video=video, 
                    caption=f"ڤیدیۆکەت ئامادەیە ✅\n\n🆔 {CHANNEL_ID}\n✨ باشترین کوالێتی و خێراترین خزمەتگوزاری",
                    reply_markup=reply_markup
                )
            os.remove(file_path)
            await msg.delete()
        else:
            await msg.edit_text("❌ نەمتوانی ڤیدیۆکە دابگرم.")
    except Exception:
        await msg.edit_text("❌ کێشەیەک ڕوویدا. دڵنیابە ڤیدیۆکە گشتییە.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats)) # تەنها بۆ ئەدمین
    
    # فلتەرکردنی هەموو شتێک جگە لە دەق
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("بۆتەکە بە هەموو تایبەتمەندییەکانەوە چالاکە...")
    app.run_polling()
    
