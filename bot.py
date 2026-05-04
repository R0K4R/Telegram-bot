import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# زانیارییەکان
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpljs3DhB_hyI"
CHANNEL_ID = "@hamaesmael"
CHANNEL_URL = "https://t.me/hamaesmael"
ADMIN_ID =58473622

async def is_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid == ADMIN_ID: return True
    try:
        m = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=uid)
        return m.status in ['member', 'administrator', 'creator']
    except: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
    await update.message.reply_text("سڵاو! بۆ داگرتنی ڤیدیۆ جۆینی کەناڵ بکە.", reply_markup=InlineKeyboardMarkup(kb))

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    if not await is_member(update, context):
        kb = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
        await update.message.reply_text("سەرەتا جۆین بکە 👇", reply_markup=InlineKeyboardMarkup(kb))
        return

    url = update.message.text
    msg = await update.message.reply_text("⏳ خەریکم ئامادەی دەکەم...")
    path = f"vid_{update.effective_user.id}.mp4"
    opts = {'format': 'best', 'outtmpl': path, 'quiet': True}

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        if os.path.exists(path):
            with open(path, 'rb') as v:
                await update.message.reply_video(video=v, caption=f"فەرموو ✅\n🆔 {CHANNEL_ID}")
            os.remove(path)
            await msg.delete()
    except Exception as e:
        await msg.edit_text(f"❌ هەڵە: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
    
