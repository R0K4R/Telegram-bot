import os
import requests
import yt_dlp
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, CallbackQueryHandler, filters, ContextTypes
from telegram.error import MessageNotModified

TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpIjs3DhB_hyI" # تۆکنەکە ڕاستەوخۆ لێرە دانراوە

# start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("📥 لینک بنێرە")

# handle link
async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.text:
        return

    url = update.message.text.strip()
    context.user_data["url"] = url

    keyboard = [
        [InlineKeyboardButton("🎥 Best", callback_data="best")],
        [InlineKeyboardButton("📺 720p", callback_data="720")],
        [InlineKeyboardButton("📱 360p", callback_data="360")],
        [InlineKeyboardButton("🎧 MP3", callback_data="mp3")]]

    await update.message.reply_text(
        "هەڵبژێرە 👇",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# button handler
async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    url = context.user_data.get("url")

    # fix TikTok short
    try:
        if "vt.tiktok.com" in url:
            url = requests.get(url).url
    except:
        pass

    msg = await query.edit_message_text("⏳ چاوەڕوان بە...")

    # format selection
    if query.data == "best":
        fmt = "bestvideo+bestaudio/best"
    elif query.data == "720":
        fmt = "bestvideo[height<=720]+bestaudio/best"
    elif query.data == "360":
        fmt = "bestvideo[height<=360]+bestaudio/best"
    else:
        fmt = "bestaudio"

    ydl_opts = {
        'format': fmt,
        'outtmpl': 'file.%(ext)s',
        'quiet': True
    }

    # MP3 processor
    if query.data == "mp3":
        ydl_opts['postprocessors'] = [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3'
        }]

    # retry
    for i in range(2):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)

            try:
                await msg.edit_text("📤 ناردن...")
            except MessageNotModified: # Handle the specific error
                pass

            if query.data == "mp3":
                await query.message.reply_audio(audio=open(filename, 'rb'))
            else:
                await query.message.reply_video(video=open(filename, 'rb'))

            os.remove(filename)
            return

        except Exception as e:
            if i == 1:
                await msg.edit_text(f"❌ هەڵە:\n{str(e)}")

# run
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle))
app.add_handler(CallbackQueryHandler(button))

print("Bot running...")
app.run_polling()
