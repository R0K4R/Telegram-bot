import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest
import yt_dlp

# --- ⚠️ زانیارییەکان لێرە بە وردی بگۆڕە ---
TOKEN = "8778519003:AAEFy9BRsvFsI_tLB2B-vcRpljs3DhB_hyI"
CHANNEL_ID = "@hamaesmael"  # یوزەرنەیمی کەناڵەکەت لێرە دابنێ
CHANNEL_URL = "https://t.me/hamaesmael" 
ADMIN_ID = 58473622  # ئایدی خۆت لێرە دابنێ (تاوەکو داوای جۆین لە تۆ نەکات)
# ---------------------------------------

USERS_FILE = "users.txt"

def add_user(user_id):
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f: f.write("")
    with open(USERS_FILE, "r") as f:
        users = f.read().splitlines()
    if str(user_id) not in users:
        with open(USERS_FILE, "a") as f:
            f.write(f"{user_id}\n")

async def is_user_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    # ئەگەر بەکارهێنەرەکە خۆت بوویت، ڕاستەوخۆ ڕێگەت پێ بدات
    if user_id == ADMIN_ID:
        return True
    try:
        member = await context.bot.get_chat_member(chat_id=CHANNEL_ID, user_id=user_id)
        return member.status in ['member', 'administrator', 'creator']
    except Exception:
        return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    add_user(update.effective_user.id)
    keyboard = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        "سڵاو! لینکێکی ڤیدیۆ (TikTok, FB, Instagram) بنێرە بۆ داگرتن.\n\n"
        "تێبینی: پێویستە جۆینی کەناڵەکەمان بکەیت بۆ بەکارهێنانی بۆتەکە.",
        reply_markup=reply_markup
    )

async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id == ADMIN_ID:
        if os.path.exists(USERS_FILE):
            with open(USERS_FILE, "r") as f:
                count = len(f.read().splitlines())
            await update.message.reply_text(f"📊 ئاماری بۆتەکە:\n\nکۆی بەکارهێنەران: {count} کەس")
        else:
            await update.message.reply_text("هێشتا هیچ ئامارێک نییە.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # ١. فلتەرکردن: تەنها دەق وەردەگرێت، وێنە و ڤیدیۆ و ڤۆیس پشتگوێ دەخات
    if not update.message.text:
        return

    user_id = update.effective_user.id
    add_user(user_id)
    url = update.message.text

    # ٢. پشکنینی جۆینی ناچاری (بۆ ئەدمین کار ناکات)
    if not await is_user_member(update, context):
        keyboard = [[InlineKeyboardButton("جۆین بە لێرە 📢", url=CHANNEL_URL)]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            "بۆ ئەوەی بتوانیت ڤیدیۆ دابگریت، دەبێت سەرەتا جۆینی کەناڵەکەمان بکەیت. 👇",
            reply_markup=reply_markup
        )
        return

    # ٣. پشکنینی لینکەکان
    valid_sites = ["tiktok.com", "facebook.com", "fb.watch", "instagram.com", "instagr.am"]
    if not any(site in url for site in valid_sites):
        return

    msg = await update.message.
    
