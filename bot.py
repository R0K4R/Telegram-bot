import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! لینکێکی یوتیوب بنێرە تا وەک موزیک بۆت دابگرم. 🎵")

async def download_audio(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    msg = await update.message.reply_text("⏳ خەریکم تاقی دەکەمەوە... تکایە چاوەڕێبە.")

    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': 'music.mp3',
        # ئەم بەشانە بۆ تێپەڕاندنی بلۆکە
        'quiet': True,
        'no_warnings': True,
        'source_address': '0.0.0.0',
        'force_ipv4': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36'
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
            
        if os.path.exists('music.mp3'):
            await msg.edit_text("📤 خەریکم بەرزی دەکەمەوە...")
            with open('music.mp3', 'rb') as audio:
                await update.message.reply_audio(audio=audio, title="تەواو بوو ✅")
            os.remove('music.mp3')
            await msg.delete()
        else:
            await msg.edit_text("❌ یوتیوب هێشتا ڕێگری دەکات. کەمێکی تر تاقی بکەرەوە.")

    except Exception as e:
        print(f"Error: {e}")
        await msg.edit_text("❌ ببورە، یوتیوب سێرڤەرەکەی بلۆک کردووە. لینکێکی تر تاقی بکەرەوە.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_audio))
    app.run_polling()
    
