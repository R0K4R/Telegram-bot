import os
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import yt_dlp

# تۆکنەکەت لێرە دابنێ
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! لینکێکی (TikTok، Facebook، یان Instagram) بنێرە بۆ ئەوەی ڤیدیۆکەت بۆ دابگرم. 📥"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    
    # پشکنینی لینکەکان
    valid_sites = ["tiktok.com", "facebook.com", "fb.watch", "instagram.com", "instagr.am"]
    if not any(site in url for site in valid_sites):
        return

    msg = await update.message.reply_text("⏳ خەریکم ڤیدیۆکە ئامادە دەکەم... تکایە چاوەڕێبە.")

    # ڕێکخستنی گشتگیر بۆ هەموو سایتەکان
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.mp4',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        file_path = 'downloaded_video.mp4'

        if os.path.exists(file_path):
            # پشکنینی قەبارەی فایل بۆ ئەوەی لە ٥٠ مێگابایت زیاتر نەبێت (بۆ تێلێگرام)
            if os.path.getsize(file_path) / (1024 * 1024) > 50:
                await msg.edit_text("⚠️ ببورە، قەبارەی ڤیدیۆکە زۆر گەورەیە و تێلێگرام ناتوانێت بینێرێت.")
            else:
                await msg.edit_text("📤 خەریکم بەرزی دەکەمەوە...")
                with open(file_path, 'rb') as video:
                    await update.message.reply_video(video=video, caption="فەرموو، ڤیدیۆکەت ئامادەیە ✅")
            
            os.remove(file_path)
            await msg.delete()
        else:
            await msg.edit_text("❌ نەمتوانی ڤیدیۆکە بدۆزمەوە. دڵنیابە ڤیدیۆکە گشتییە (Public).")

    except Exception as e:
        print(f"Error: {e}")
        await msg.edit_text("❌ هەڵەیەک ڕوویدا. ڕەنگە ڤیدیۆکە پارێزراو بێت یان لینکەکە هەڵە بێت.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    print("بۆتی گشتگیر چالاکە...")
    app.run_polling()
    
