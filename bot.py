import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# --- زانیارییەکان ---
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"
CHANNEL_ID = "@hamaesmael"
CHANNEL_URL = "https://t.me/hamaesmael"
ADMIN_ID = 58473622
# ------------------

async def is_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid == ADMIN_ID: return True
    try:
        m = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=uid)
        return m.status in ['member', 'administrator', 'creator']
    except: return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
    await update.message.reply_text(
        "سڵاو! بۆ داگرتنی ڤیدیۆ لە (تیکتۆک، فەیسبووک، ئینستاگرام) جۆینی کەناڵ بکە و لینکەکە بنێرە.",
        reply_markup=InlineKeyboardMarkup(kb)
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text: return
    uid = update.effective_user.id
    
    if not await is_member(update, context):
        kb = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
        await update.message.reply_text("بۆ بەکارهێنانی بۆتەکە، سەرەتا جۆینی کەناڵەکەمان بکە. 👇", reply_markup=InlineKeyboardMarkup(kb))
        return

    url = update.message.text
    if not any(s in url for s in ["tiktok.com", "facebook.com", "fb.watch", "instagram.com"]): return

    msg = await update.message.reply_text("⏳ خەریکم ڤیدیۆکە ئامادە دەکەم...")
    path = f"vid_{uid}.mp4"
    opts = {
        'format': 'best',
        'outtmpl': path,
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            ydl.download([url])
        if os.path.exists(path):
            kb = [[InlineKeyboardButton("ناردن بۆ هاوڕێیان 🚀", url=f"https://t.me/share/url?url={CHANNEL_URL}")]]
            with open(path, 'rb') as v:
                await update.message.reply_video(video=v, caption=f"ڤیدیۆکەت ئامادەیە ✅\n\n🆔 {CHANNEL_ID}", reply_markup=InlineKeyboardMarkup(kb))
            os.remove(path)
            await msg.delete()
        else:
            await msg.edit_text("❌ کێشەیەک لە داگرتن هەبوو.")
    except Exception as e:
        await msg.edit_text(f"❌ هەڵە: ڤیدیۆکە دانابەزێت یان تایبەتە (Private).")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("بۆتەکە بێ کێشە کار دەکات...")
    app.run_polling()
    
