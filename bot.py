import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# تۆکنەکەت لێرە دابنێ
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("سڵاو! لینکێکی تیکتۆک بنێرە بۆ ئەوەی ڤیدیۆکەت بەبێ نیشانە بۆ دابگرم. 📥")

async def download_tiktok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "tiktok.com" not in url:
        return

    msg = await update.message.reply_text("⏳ خەریکم ڤیدیۆکە ئامادە دەکەم... تکایە چاوەڕێبە.")

    # ڕێکخستنی تایبەت بۆ تیکتۆک
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'tiktok_video.mp4',
        'quiet': True,
        'no_warnings': True,
    }

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        file_path = 'tiktok_video.mp4'

        if os.path.exists(file_path):
            await msg.edit_text("📤 خەریکم بەرزی دەکەمەوە...")
            with open(file_path, 'rb') as video:
                await update.message.reply_video(video=video, caption="ڤیدیۆکەت ئامادەیە ✅")
            os.remove(file_path)
            await msg.delete()
        else:
            await msg.edit_text("❌ ببورە، کێشەیەک لە داگرتنی ڤیدیۆکە هەبوو.")

    except Exception as e:
        print(f"Error: {e}")
        await msg.edit_text("❌ هەڵەیەک ڕوویدا، دڵنیابە لینکەکە ڕاستە.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_tiktok))
    print("بۆتی تیکتۆک چالاکە...")
    app.run_polling()
    
