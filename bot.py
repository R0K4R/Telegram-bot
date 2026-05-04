import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# --- زانیارییەکان ---
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpljs3DhB_hyI"
CHANNEL_ID = "@hamaesmael"
CHANNEL_URL = "https://t.me/hamaesmael"
ADMIN_ID = 58473622
# ------------------

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
    if user_id == ADMIN_ID: return True
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)
    kb = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
    await update.message.reply_text("سڵاو! بۆ داگرتنی ڤیدیۆ جۆینی کەناڵ بکە.", reply_markup=InlineKeyboardMarkup(kb))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    user_id = update.effective_user.id
    add_user(user_id)
    
    if not await is_user_member(update, context):
        kb = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
        await update.message.reply_text("سەرەتا جۆین بکە 👇", reply_markup=InlineKeyboardMarkup(kb))
        return

    url = update.message.text
    if not any(s in url for s in ["tiktok.com", "facebook.com", "instagram.com"]): return

    msg = await update.message.reply_text("⏳ خەریکم ئامادەی دەکەم...")
    file_path = f"vid_{user_id}.mp4"
    ydl_opts = {'format': 'best', 'outtmpl': file_path, 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        if os.path.exists(file_path):
            kb = [[InlineKeyboardButton("ناردن بۆ هاوڕێیان 🚀", url=f"https://t.me/share/url?url={CHANNEL_URL}")]]
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video, caption=f"فەرموو ✅\n\n🆔 {CHANNEL_ID}", reply_markup=InlineKeyboardMarkup(kb))
            os.remove(file_path)
            await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ هەڵە ڕوویدا: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    
