import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# دالة التحميل الأساسية
def download_media(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'file.mp4',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return

    # رسالة اعتذار لليوتيوب فقط بسبب حظر السيرفرات
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text("⚠️ نعتذر، التحميل من يوتيوب متوقف حالياً. جرب تيك توك أو إنستغرام.")
        return

    try:
        # التحميل المباشر
        path = download_media(url)
        with open(path, 'rb') as video:
            # هنا يمكنك تغيير نص الرد النهائي
            await update.message.reply_video(video=video, caption="🎬 مشاهدة ممتعة)
        os.remove(path)
    except Exception as e:
        await update.message.reply_text("❌ حدث خطأ في الرابط أو أن الفيديو غير متاح.")

if __name__ == '__main__':
    # تأكد من وضع التوكن الخاص بك هنا بدقة
    TOKEN = "8351715808:AAHYmi3NxfLYKI6m5kAdh_gO9eWu-tOQ5mQ" 
    
    print("البوت يعمل الآن على Railway... 🚀")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)
