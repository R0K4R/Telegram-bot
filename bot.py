from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, filters, ContextTypes
import yt_dlp
import os

# تۆکنەکەت لێرە دابنێ
TOKEN = "8778519003:AAEL_Xu8AB3B8d-MQXvjcI_9Sl__mTjtukw"

# فرمانی /start بۆ ناردنی نامەی بەخێرهاتن و دوگمە
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("کەناڵی تێلێگرام", url="https://t.me/example")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text="سڵاو! بەخێربێیت بۆ بۆتی داگرتنی ڤیدیۆ.\nتکایە لینکێک بنێرە بۆ داگرتن.",
        reply_markup=reply_markup
    )

# فەنکشن بۆ وەرگرتنی لینک و داگرتنی ڤیدیۆ
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("خەریکم ڤیدیۆکە ئامادە دەکەم... تکایە چاوەڕێبە ⏳")
        
        # لێرەدا کۆدی yt-dlp بەکاردێت بۆ داگرتن (نموونەیەکی سادە)
        ydl_opts = {'format': 'best', 'outtmpl': 'video.mp4'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        # ناردنی ڤیدیۆکە بۆ بەکارهێنەر
        await update.message.reply_video(video=open('video.mp4', 'rb'))
        os.remove('video.mp4') # سڕینەوەی فایلەکە دوای ناردن
    else:
        await update.message.reply_text("تکایە لینکێکی ڕاست و دروستی یوتیوب بنێرە.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), handle_message))
    
    print("بۆتەکە چالاکە...")
    app.run_polling()
    
