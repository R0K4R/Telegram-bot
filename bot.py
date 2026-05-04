import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import yt_dlp

# تۆکنەکەت لێرە دابنێ
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "سڵاو! لینکێکی (TikTok، FB، یان Instagram) بنێرە. 📥\n"
        "دوای داگرتن دەتوانیت ڤیدیۆکە بکەیت بە موزیکیش! 🎵"
    )

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    valid_sites = ["tiktok.com", "facebook.com", "fb.watch", "instagram.com", "instagr.am"]
    
    if not any(site in url for site in valid_sites):
        return

    msg = await update.message.reply_text("⏳ خەریکم ڤیدیۆکە ئامادە دەکەم...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'vid_{update.effective_user.id}.mp4',
        'quiet': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36',
    }

    try:
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, lambda: yt_dlp.YoutubeDL(ydl_opts).download([url]))
        
        file_path = f'vid_{update.effective_user.id}.mp4'

        if os.path.exists(file_path):
            keyboard = [
                [InlineKeyboardButton("گۆڕین بۆ موزیک 🎵", callback_data=f"mp3_{file_path}")],
                [InlineKeyboardButton("کەناڵی ئێمە 📢", url="https://t.me/hamaesmael")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)

            with open(file_path, 'rb') as video:
                await update.message.reply_video(
                    video=video, 
                    caption="ڤیدیۆکەت ئامادەیە ✅\nلە لایەن: @Save_Kurd_Bot",
                    reply_markup=reply_markup
                )
            await msg.delete()
            # لێرە فایلەکە ناسڕینەوە تاوەکو ئەگەر ویستی بیکات بە MP3 بەکاری بێنینەوە
        else:
            await msg.edit_text("❌ هەڵەیەک ڕوویدا.")

    except Exception as e:
        await msg.edit_text("❌ نەمتوانی ڤیدیۆکە دابگرم.")

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data.startswith("mp3_"):
        vid_path = query.data.replace("mp3_", "")
        mp3_path = vid_path.replace(".mp4", ".mp3")
        
        if os.path.exists(vid_path):
            await query.edit_message_caption(caption="⏳ خەریکم دەیکەم بە موزیک...")
            
            # بەکارهێنانی FFmpeg بۆ گۆڕین
            cmd = f"ffmpeg -i {vid_path} -vn -ar 44100 -ac 2 -b:a 192k {mp3_path} -y"
            os.system(cmd)
            
            with open(mp3_path, 'rb') as audio:
                await query.message.reply_audio(audio=audio, title="موزیکی ڤیدیۆکە")
            
            if os.path.exists(vid_path): os.remove(vid_path)
            if os.path.exists(mp3_path): os.remove(mp3_path)
        else:
            await query.message.reply_text("❌ فایلەکە نەدۆزرایەوە، تکایە دووبارە لینکەکە بنێرە.")

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    app.add_handler(CallbackQueryHandler(button_handler))
    print("بۆتی پڕۆفیشناڵ چالاکە...")
    app.run_polling()
    
