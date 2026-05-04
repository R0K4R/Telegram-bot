import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# تۆکنەکەت لێرە لە نێوان دوو کەوانەکە دابنێ
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! لینکێکی یوتیوب بنێرە بۆ ئەوەی بە شێوەی موزیک (MP3) بۆت دابگرم. 🎵")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith(("http://", "https://")):
        return

    msg = await update.message.reply_text("⏳ خەریکم وەک موزیک ئامادەی دەکەم... تکایە چاوەڕێبە.")

    # ڕێکخستنی زیرەک بۆ داگرتنی موزیک و تێپەڕاندنی بلۆک
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'music.%(ext)s',
        # ئەم بەشە وای لێ دەکات یوتیوب وا بزانێت تۆ مۆبایلی نەک سێرڤەر
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36',
        'nocheckcertificate': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        # بەکارهێنانی loop بۆ ئەوەی سێرڤەرەکە نەوەستێت
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        file_path = 'music.mp3'

        if os.path.exists(file_path):
            await msg.edit_text("📤 خەریکم موزیکەکە بەرز دەکەمەوە...")
            with open(file_path, 'rb') as audio:
                await update.message.reply_audio(
                    audio=audio, 
                    title="گۆرانییەکە ئامادەیە",
                    performer="Save_Kurd_Bot"
                )
            os.remove(file_path)
            await msg.delete()
        else:
            await msg.edit_text("❌ ببورە، فایلەکە دروست نەکرا. تکایە لینکێکی تر تاقی بکەرەوە.")

    except Exception as e:
        print(f"Error: {e}")
        await msg.edit_text("❌ یوتیوب ڕێگری لە داگرتنی ئەم لینکە کرد. کەمێکی تر هەوڵ بدەرەوە.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    print("بۆتەکە دەستی پێکرد...")
    app.run_polling()
    
    
