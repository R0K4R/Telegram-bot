import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# تۆکنەکەت لێرە دابنێ
TOKEN = "8778519003:AAEL_Xu8AB3B8d-MQXvjcI_9Sl__mTjtukw"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! لینکێکی یوتیوب بنێرە بۆ ئەوەی بە شێوەی دەنگ (MP3) بۆت دابگرم. 🎵")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith(("http://", "https://")):
        return

    msg = await update.message.reply_text("⏳ خەریکم وەک موزیک ئامادەی دەکەم... تکایە چاوەڕێبە.")

    # ڕێکخستنی yt-dlp بۆ تەنها دەنگ
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'music.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            file_path = 'music.mp3'

            await msg.edit_text("📤 خەریکم موزیکەکە بەرز دەکەمەوە...")
            with open(file_path, 'rb') as audio:
                await update.message.reply_audio(
                    audio=audio, 
                    title=info.get('title', 'موزیک'),
                    performer=info.get('uploader', 'Save_kurd')
                )
            
            os.remove(file_path)
            await msg.delete()

    except Exception as e:
        await msg.edit_text(f"❌ ببورە، کێشەیەک لە داگرتنی ئەم لینکە هەیە.")
        print(f"Error: {e}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    print("بۆتی موزیک چالاکە...")
    app.run_polling()
    
